"""
Utilities for running jobs and managing crew execution.
"""
import json
from datetime import datetime, UTC
from typing import Dict, Any
from sqlalchemy.orm import Session
from crewai import Crew
import logging
from enum import Enum
import litellm
import os
import traceback

from .. import database
from ..utils.logger_manager import LoggerManager
from ..utils.event_loop import run_in_thread_with_loop
from ..utils.crew_helpers import (
    configure_process_output_handler,
    setup_api_key,
    enable_verbose_callbacks,
    configure_task_callbacks
)
from ..utils.task_tracker import TaskStatus, update_task_status
from ..crew import Backendcrew
from ..utils.api_key_utils import setup_all_api_keys
from ..llm_config import LLMConfig, ModelProvider
from ..database import SessionLocal

# Initialize logger manager
logger_manager = LoggerManager()

# To be used by the jobs.py module
jobs = {}

# Job status enum
class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

def _run_job_sync(job_id: str, config: Any, db: Session, crew: Crew):
    """Execute the job synchronously."""
    # Note: This function will be called in a thread, so we wrap it with
    # run_in_thread_with_loop to handle event loops appropriately
    
    def execute_job():
        try:
            # First, clear any existing API keys from environment to prevent cross-provider contamination
            logger_manager.crew.info("[API_KEYS_RESET] Clearing existing API keys from environment")
            for key_name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "DATABRICKS_TOKEN"]:
                if key_name in os.environ:
                    logger_manager.crew.info(f"[API_KEYS_RESET] Removing {key_name} from environment")
                    del os.environ[key_name]
            
            # Reset LiteLLM settings through LLMConfig
            LLMConfig.initialize()
            
            # Set up all API keys from database
            setup_all_api_keys(db)
            
            # Initialize LLMConfig which applies the litellm patch
            LLMConfig.initialize()
            
            # Add debug logging for LiteLLM configuration
            logger_manager.crew.info("[LITELLM DEBUG] Checking LiteLLM configuration")
            logger_manager.crew.info(f"[LITELLM DEBUG] LiteLLM version: {litellm.__version__ if hasattr(litellm, '__version__') else 'unknown'}")
            logger_manager.crew.info(f"[LITELLM DEBUG] Current environment variables:")
            for env_var in ['OPENAI_API_KEY', 'OPENAI_API_BASE', 'DEEPSEEK_API_KEY', 'DEEPSEEK_API_BASE', 'ANTHROPIC_API_KEY']:
                if env_var in os.environ:
                    if env_var == 'ANTHROPIC_API_KEY':
                        key = os.environ[env_var]
                        if key.startswith('sk-ant-'):
                            logger_manager.crew.info(f"[LITELLM DEBUG] {env_var} is set and has correct format")
                        else:
                            logger_manager.crew.warning(f"[LITELLM DEBUG] {env_var} is set but doesn't start with 'sk-ant-'. This is unusual but may work if using a newer key format.")
                    else:
                        logger_manager.crew.info(f"[LITELLM DEBUG] {env_var} is set")
                else:
                    logger_manager.crew.info(f"[LITELLM DEBUG] {env_var} is NOT set")
            
            # Inspect the model configuration for each task 
            for task in crew.tasks:
                if hasattr(task, 'agent') and task.agent:
                    agent = task.agent
                    logger_manager.crew.info(f"[TASK DEBUG] Task {task.description[:30]}... using agent with model: {getattr(agent, 'model', 'unknown')}")
                    if hasattr(agent, '_llm'):
                        llm_info = str(agent._llm.__dict__)
                        logger_manager.crew.info(f"[TASK DEBUG] Agent LLM details: {llm_info[:200]}...")

            # Execute crew tasks using the provided crew instance
            logger_manager.crew.info("Starting crew execution")
            
            # Get the job callback from the crew process
            job_callback = crew.process.output_callback
            if job_callback:
                logger_manager.crew.info("Found job callback, triggering initial output")
                # Instead of calling the async method directly, use a synchronous wrapper
                if hasattr(job_callback, 'execute'):
                    # For JobOutputCallback which has an async execute method
                    import asyncio
                    try:
                        # Use run_until_complete to handle the async execute method
                        asyncio.run(job_callback.execute("Starting crew execution..."))
                    except RuntimeError:
                        # If there's already an event loop running, use a different approach
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            # Create a new event loop for this thread if needed
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            new_loop.run_until_complete(job_callback.execute("Starting crew execution..."))
                            new_loop.close()
                        else:
                            loop.run_until_complete(job_callback.execute("Starting crew execution..."))
                else:
                    # For regular callbacks that are not async
                    job_callback("Starting crew execution...")

                # Set up process output handler
                process_output = configure_process_output_handler(job_callback)

                # Set the process output handler for crew and all tasks
                crew.process.output_callback = process_output
                crew.process.verbose = True
                
                # Set up callbacks for all tasks and their components
                for task in crew.tasks:
                    if hasattr(task, 'process'):
                        task.process.output_callback = process_output
                        task.process.verbose = True
                    
                    if hasattr(task, 'agent'):
                        agent = task.agent
                        if hasattr(agent, 'process'):
                            agent.process.output_callback = process_output
                            agent.process.verbose = True
                        
                        if hasattr(agent, 'tools'):
                            for tool in agent.tools:
                                if hasattr(tool, 'process'):
                                    tool.process.output_callback = process_output
                                    tool.process.verbose = True

            # Execute the crew using the standard kickoff method
            # The patched litellm.completion will handle provider switching
            result = crew.kickoff()
            logger_manager.crew.info("Crew execution completed")
            
            # Handle the result
            result_str = {}
            if isinstance(result, list):
                # Process list of results
                for i, output in enumerate(result):
                    if hasattr(output, 'output'):
                        result_str[f"task_{i}"] = output.output
                    else:
                        result_str[f"task_{i}"] = str(output)
            elif hasattr(result, 'output'):
                # Process single task output
                result_str = {"result": result.output}
            else:
                # Process any other type of result
                result_str = {"result": str(result)}
            
            # Update in-memory job status
            if job_id in jobs:
                jobs[job_id]["status"] = JobStatus.COMPLETED.value
                jobs[job_id]["result"] = result_str
            
            db_run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
            if db_run:
                db_run.status = JobStatus.COMPLETED.value
                db_run.result = result_str
                db_run.completed_at = datetime.now(UTC)
                db.commit()
            
            return result_str
            
        except Exception as e:
            logger_manager.crew.error(f"Error in job {job_id}: {str(e)}")
            
            # Mark any running tasks as failed
            try:
                # Find all tasks with 'running' status
                running_tasks = db.query(database.TaskStatus).filter(
                    database.TaskStatus.job_id == job_id,
                    database.TaskStatus.status == TaskStatus.RUNNING
                ).all()
                
                # Update their status to failed
                for task in running_tasks:
                    logger_manager.crew.info(f"Marking task {task.task_id} as failed due to job error")
                    update_task_status(db, job_id, task.task_id, TaskStatus.FAILED)
            except Exception as task_error:
                logger_manager.crew.error(f"Error updating task statuses on job failure: {str(task_error)}")
            
            if job_id in jobs:
                jobs[job_id]["status"] = JobStatus.FAILED.value
                jobs[job_id]["error"] = str(e)
            
            db_run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
            if db_run:
                db_run.status = JobStatus.FAILED.value
                db_run.error = str(e)
                db_run.completed_at = datetime.now(UTC)
                db.commit()
            
            raise
    
    # Use our wrapper to handle event loops properly in threads
    return run_in_thread_with_loop(execute_job)

async def prepare_and_run_crew(job_id: str, config: Any, db: Session, streaming_cb):
    """Set up the crew with all callbacks and configuration, then run it."""
    try:
        logger_manager.crew.info(f"Setting up crew for job {job_id}")
        
        # Set up all API keys from database
        setup_all_api_keys(db)
        
        # Debug the provider configuration before starting
        provider = LLMConfig.get_provider()
        logger_manager.crew.info(f"[PROVIDER DEBUG] Current LLMConfig provider before job: {provider}")
        
        # Our litellm patch will handle provider switching dynamically
        # No need to force a specific provider globally
        
        # Update status to running
        if job_id in jobs:
            jobs[job_id]["status"] = JobStatus.RUNNING.value
        
        db_run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
        if not db_run:
            raise Exception(f"Run record not found for job {job_id}")
            
        db_run.status = JobStatus.RUNNING.value
        db.commit()

        # Get configuration from database
        stored_config = db_run.inputs
        if not stored_config:
            raise Exception("No configuration found in database")
            
        agents_yaml = stored_config.get("agents_yaml")
        tasks_yaml = stored_config.get("tasks_yaml")
        
        if not agents_yaml or not tasks_yaml:
            raise Exception("Invalid configuration: missing agents or tasks")

        # Ensure each agent has a model specified or use default
        for agent_key, agent in agents_yaml.items():
            if 'model' not in agent:
                # Default to GPT-4 if no model specified
                agent['model'] = "gpt-4"
            logger_manager.crew.info(f"Agent {agent_key} using model: {agent['model']}")
            
            # Add more detailed logging about the model configuration
            logger_manager.crew.info(f"[MODEL DEBUG] Agent {agent_key} model details:")
            logger_manager.crew.info(f"[MODEL DEBUG] Raw model name: {agent['model']}")
            provider = LLMConfig.get_provider()
            logger_manager.crew.info(f"[MODEL DEBUG] Current provider: {provider}")
            logger_manager.crew.info(f"[MODEL DEBUG] API base: {LLMConfig.get_api_base()}")
            formatted_model = LLMConfig.get_model_name_for_crewai(agent['model'])
            logger_manager.crew.info(f"[MODEL DEBUG] Formatted model for CrewAI: {formatted_model}")

        # Configure callbacks for each task
        for task_key, task in tasks_yaml.items():
            logger_manager.crew.info(f"Configuring task: {task_key}")
            
            # Get agent configuration for this task
            agent_key = task.get('agent')
            if not agent_key or agent_key not in agents_yaml:
                logger_manager.crew.error(f"Agent '{agent_key}' not found for task '{task_key}'")
                continue
                
            agent_config = agents_yaml[agent_key]
            configure_task_callbacks(task_key, task, agent_config, db, job_id)

        # Update stored configuration with callbacks
        stored_config["tasks_yaml"] = tasks_yaml
        db_run.inputs = stored_config
        db.commit()

        # Initialize the crew instance directly with job_id and configurations
        crew_instance = Backendcrew(job_id=job_id, agents_yaml=agents_yaml, tasks_yaml=tasks_yaml)
        crew = crew_instance.crew()
        
        # Enable verbose callbacks for all crew components
        enable_verbose_callbacks(crew, streaming_cb)
        logger_manager.crew.info("All callbacks and verbose modes configured")

        # Execute the job synchronously in the thread pool
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        
        # Get the current event loop
        current_loop = asyncio.get_running_loop()
        thread_pool = ThreadPoolExecutor(max_workers=10)
        
        # Run the actual job in a thread pool to prevent blocking
        try:
            result = await current_loop.run_in_executor(
                thread_pool, 
                _run_job_sync, 
                job_id, 
                config, 
                db, 
                crew
            )
            
            logger_manager.crew.info(f"Job {job_id} completed successfully")
            return result
            
        except Exception as e:
            logger_manager.crew.error(f"Thread pool execution failed for job {job_id}: {str(e)}")
            raise
    
    except Exception as e:
        logger_manager.crew.error(f"Error preparing crew for job {job_id}: {str(e)}")
        
        if job_id in jobs:
            jobs[job_id]["status"] = JobStatus.FAILED.value
            jobs[job_id]["error"] = str(e)
        
        try:
            db_run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
            if db_run:
                db_run.status = JobStatus.FAILED.value
                db_run.error = str(e)
                db_run.completed_at = datetime.now(UTC)
                db.commit()
        except Exception as db_error:
            logger_manager.crew.error(f"Failed to update database with error status: {str(db_error)}")
            
        raise 