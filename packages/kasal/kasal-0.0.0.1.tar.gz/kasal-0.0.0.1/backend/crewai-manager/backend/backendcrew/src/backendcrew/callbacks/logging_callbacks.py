from typing import Any, Optional
from datetime import datetime
from .base import BaseCallback
import logging
from sqlalchemy.orm import Session
import asyncio

logger = logging.getLogger(__name__)

class AgentTraceCallback(BaseCallback):
    """Logs agent traces to the database."""
    
    def __init__(self, db: Session, job_id: str, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.job_id = job_id
    
    async def execute(self, output: Any) -> None:
        """Execute the callback asynchronously."""
        try:
            logger.info(f"=== AgentTraceCallback Processing Output ===")
            logger.info(f"Output type: {type(output)}")
            logger.info(f"Output dir: {dir(output)}")
            
            # Extract agent information
            agent_info = getattr(output, 'agent', None)
            logger.info(f"Agent info: {agent_info}")
            
            # Get agent name with detailed logging
            agent_name = None
            if agent_info:
                if hasattr(agent_info, 'role'):
                    agent_name = agent_info.role
                    logger.info(f"Got agent name from role: {agent_name}")
                elif hasattr(agent_info, 'name'):
                    agent_name = agent_info.name
                    logger.info(f"Got agent name from name: {agent_name}")
            if not agent_name and isinstance(agent_info, str):
                agent_name = agent_info
                logger.info(f"Got agent name from string: {agent_name}")
            if not agent_name:
                agent_name = getattr(output, 'agent_name', 'Unknown Agent')
                logger.info(f"Using fallback agent name: {agent_name}")

            # Get task information with detailed logging
            task_name = None
            if hasattr(output, 'task'):
                task = getattr(output, 'task')
                if hasattr(task, 'description'):
                    task_name = task.description
                    logger.info(f"Got task name from task.description: {task_name}")
                elif hasattr(task, 'name'):
                    task_name = task.name
                    logger.info(f"Got task name from task.name: {task_name}")
            if not task_name:
                task_name = getattr(output, 'description', None)
                logger.info(f"Got task name from output.description: {task_name}")
            if not task_name:
                task_name = self.task_key or 'unknown_task'
                logger.info(f"Using fallback task name: {task_name}")

            # Get output content with detailed logging
            output_content = None
            if hasattr(output, 'output'):
                output_content = output.output
                logger.info("Got output from output.output")
            elif hasattr(output, 'raw'):
                output_content = output.raw
                logger.info("Got output from output.raw")
            elif hasattr(output, 'result'):
                output_content = output.result
                logger.info("Got output from output.result")
            else:
                output_content = str(output)
                logger.info("Using str(output) as fallback")
            
            logger.info(f"Output content length: {len(str(output_content))}")
            logger.info(f"Output content preview: {str(output_content)[:200]}...")

            # Create the trace with detailed logging
            from ..database import Run, Trace
            db_run = self.db.query(Run).filter(Run.job_id == self.job_id).first()
            if db_run:
                logger.info(f"Found run record with ID: {db_run.id}")
                
                trace = Trace(
                    run_id=db_run.id,
                    agent_name=agent_name,
                    task_name=task_name,
                    output=output_content,
                    created_at=datetime.now()
                )
                self.db.add(trace)
                self.db.commit()
                
                logger.info(f"Successfully created trace:")
                logger.info(f"- Run ID: {db_run.id}")
                logger.info(f"- Agent: {agent_name}")
                logger.info(f"- Task: {task_name}")
                logger.info(f"- Content Length: {len(str(output_content))}")
            else:
                logger.error(f"No run record found for job_id: {self.job_id}")
                
            logger.info("=== End AgentTraceCallback Processing ===")
            
            # Return the output to allow chaining
            return output
            
        except Exception as e:
            logger.error(f"Error in agent trace callback: {str(e)}")
            logger.error("Stack trace:", exc_info=True)
            raise

class TaskCompletionLogger(BaseCallback):
    """Logs task completion with detailed output information."""
    
    async def execute(self, output: Any) -> Any:
        """Execute the callback asynchronously."""
        try:
            self._log_output_info(output)
            self.metadata['completion_time'] = datetime.now().isoformat()
            return output
        except Exception as e:
            logger.error(f"Error in task completion logging: {str(e)}")
            logger.error("Stack trace:", exc_info=True)
            raise

class DetailedOutputLogger(BaseCallback):
    """Logs detailed analysis of the output structure and content."""
    
    async def execute(self, output: Any) -> Any:
        """Execute the callback asynchronously."""
        try:
            logger.info("=== Detailed Output Analysis ===")
            
            # Safe attributes to inspect
            safe_attributes = [
                'description',
                'name',
                'expected_output',
                'summary',
                'raw',
                'agent',
                'task_key',
                'output'
            ]
            
            # Log basic output information
            logger.info(f"Output Type: {type(output)}")
            
            # Safely inspect attributes
            for attr_name in safe_attributes:
                try:
                    if hasattr(output, attr_name):
                        attr = getattr(output, attr_name)
                        attr_type = type(attr)
                        if isinstance(attr, (str, int, float, bool)):
                            # For simple types, log the actual value
                            preview = str(attr)[:100] + "..." if len(str(attr)) > 100 else str(attr)
                            logger.info(f"Attribute: {attr_name} (Type: {attr_type}) = {preview}")
                        else:
                            # For complex types, just log the type
                            logger.info(f"Attribute: {attr_name} (Type: {attr_type})")
                except Exception as e:
                    logger.debug(f"Could not access attribute {attr_name}: {str(e)}")
            
            # Log output content if available
            try:
                if hasattr(output, 'raw'):
                    content = output.raw
                    logger.info(f"Content Length: {len(str(content))}")
                    logger.info(f"Content Preview: {str(content)[:200]}...")
            except Exception as e:
                logger.debug(f"Could not access output content: {str(e)}")
            
            logger.info("=== End Detailed Analysis ===")
            
            # Return the output to allow chaining
            return output
            
        except Exception as e:
            logger.error(f"Error in detailed output analysis: {str(e)}")
            logger.error("Stack trace:", exc_info=True)
            raise 