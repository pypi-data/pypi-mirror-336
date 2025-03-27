from typing import Any
from datetime import datetime, UTC
from .base import BaseCallback
import json
import sys
import io
import logging
from logging.handlers import MemoryHandler
from .. import database
from ..utils.logger_manager import LoggerManager

# Initialize logger manager
logger_manager = LoggerManager()

class LogCaptureHandler(logging.Handler):
    """Captures all log records for a specific job."""
    
    def __init__(self, job_id: str):
        super().__init__()
        self.job_id = job_id
        self.db = database.SessionLocal()
        self.buffer = []
        self.buffer_size = 50  # Maximum number of individual log entries to hold
        
    def emit(self, record):
        """Buffer the log record"""
        try:
            # Format the log message
            message = self.format(record)
            if message.strip():  # Only add non-empty messages
                self.buffer.append((message, record.created))
            
            # Flush if buffer is full
            if len(self.buffer) >= self.buffer_size:
                self.flush()
                
        except Exception as e:
            logger_manager.system.error(f"Error buffering log record: {e}", exc_info=True)
    
    def _group_logs_by_time(self):
        """Group logs into time windows and combine them."""
        if not self.buffer:
            return []
        
        # Sort buffer by timestamp
        sorted_buffer = sorted(self.buffer, key=lambda x: x[1])
        grouped_logs = []
        current_group = []
        current_time = sorted_buffer[0][1]
        time_window = 2.0  # Time window in seconds to group logs
        
        for message, timestamp in sorted_buffer:
            # If message is within time window, add to current group
            if timestamp - current_time <= time_window:
                current_group.append(message)
            else:
                # Create new group and update current time
                if current_group:
                    grouped_logs.append((current_group, current_time))
                current_group = [message]
                current_time = timestamp
        
        # Add last group
        if current_group:
            grouped_logs.append((current_group, current_time))
        
        return grouped_logs
    
    def flush(self):
        """Write all buffered records to the database in a batch"""
        if not self.buffer:
            return
            
        try:
            # Group logs by time window
            grouped_logs = self._group_logs_by_time()
            
            # Create job output records for each group
            job_outputs = [
                database.JobOutput(
                    job_id=self.job_id,
                    output="\n".join(messages),  # Combine messages with newlines
                    timestamp=datetime.fromtimestamp(group_time, UTC)
                )
                for messages, group_time in grouped_logs
            ]
            
            if job_outputs:  # Only commit if we have records to insert
                self.db.bulk_save_objects(job_outputs)
                self.db.commit()
            
            self.buffer.clear()
            
        except Exception as e:
            logger_manager.system.error(f"Error persisting logs to database: {e}", exc_info=True)
            try:
                self.db.rollback()
            except:
                pass
    
    def close(self):
        """Clean up resources"""
        try:
            # Flush any remaining records
            self.flush()
            self.db.close()
        finally:
            super().close()

class JobOutputCallback(BaseCallback):
    """Callback for streaming job output to the database."""
    
    def __init__(self, job_id: str, max_retries: int = 3):
        super().__init__(max_retries)
        self.job_id = job_id
        
        # Create and configure the log handler
        self.log_handler = LogCaptureHandler(job_id)
        self.log_handler.setFormatter(
            logging.Formatter(
                '[%(name)s] %(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        )
        
        # Add handler to all relevant loggers (excluding API logs)
        logger_manager.crew.addHandler(self.log_handler)
        logger_manager.llm.addHandler(self.log_handler)
        logging.getLogger('backendcrew').addHandler(self.log_handler)
        logging.getLogger('LiteLLM').addHandler(self.log_handler)
        logging.getLogger('httpx').addHandler(self.log_handler)
        
        logger_manager.system.info(f"Initialized JobOutputCallback for job {job_id}")

    async def execute(self, output: Any) -> Any:
        """Process, persist, and return the output."""
        try:
            # Convert output to string based on its type
            if hasattr(output, 'raw'):
                message = output.raw
            elif isinstance(output, dict):
                message = json.dumps(output)  # Remove indent for more compact logs
            else:
                message = str(output)

            # Log the output through the crew logger
            if message.strip():  # Only log non-empty messages
                logger_manager.crew.info(message)
            
            # Ensure we always return the original output, not the processed message
            return output

        except Exception as e:
            logger_manager.system.error(f"Error processing output for job {self.job_id}: {e}", exc_info=True)
            # Even in case of error, return the original output to ensure data flow
            return output

    def __del__(self):
        """Clean up logging handler when callback is destroyed."""
        try:
            # Remove our handler from all loggers
            logger_manager.crew.removeHandler(self.log_handler)
            logger_manager.llm.removeHandler(self.log_handler)
            logging.getLogger('backendcrew').removeHandler(self.log_handler)
            logging.getLogger('LiteLLM').removeHandler(self.log_handler)
            self.log_handler.close()
        except Exception as e:
            logger_manager.system.error(f"Error cleaning up JobOutputCallback: {e}", exc_info=True) 