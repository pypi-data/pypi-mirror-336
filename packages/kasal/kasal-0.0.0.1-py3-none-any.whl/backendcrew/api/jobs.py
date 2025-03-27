from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, ConfigDict
import yaml
from typing import Dict, Optional, Type, List, Any
from pathlib import Path
import tempfile
import shutil
import uuid
import os
from datetime import datetime, UTC
from enum import Enum
from sqlalchemy.orm import Session
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
import openai
import litellm
from openai import OpenAI
from crewai import Agent, Crew, Process, Task

from .. import database
from ..llm_config import LLMConfig, ModelProvider, SUPPORTED_MODELS
from ..utils.logger_manager import LoggerManager
from ..callbacks import (
    BaseCallback,
    CallbackFailedError,
    TaskCompletionLogger,
    DetailedOutputLogger,
    SchemaValidator,
    ContentValidator,
    TypeValidator,
    JsonFileStorage,
    DatabaseStorage,
    FileSystemStorage,
    OutputFormatter,
    DataExtractor,
    OutputEnricher,
    OutputSummarizer,
    AgentTraceCallback,
    JobOutputCallback
)
from ..crew import Backendcrew
from ..flow import Backendflow
from .generate_job_name import generate_run_name
# Import utility functions from utility modules
from ..utils.crew_helpers import (
    validate_model,
    configure_task_callbacks,
    enable_verbose_callbacks,
    setup_api_key,
    configure_process_output_handler,
    convert_tool_ids,
    order_tasks_by_dependencies,
    validate_tasks_and_agents
)
from ..utils.job_runner import _run_job_sync, JobStatus
# Import the task tracker module
from ..utils.task_tracker import create_task_statuses_for_job


# Initialize router, logger, and other global resources
router = APIRouter()
logger_manager = LoggerManager()
# Initialize LLMConfig with provider switching
LLMConfig.initialize()
client = OpenAI(
    api_key=LLMConfig.get_api_key(),
    base_url=LLMConfig.get_api_base() if LLMConfig.get_api_base() else None
)
jobs = {}  # In-memory job storage (in production, use a proper database)
thread_pool = ThreadPoolExecutor(max_workers=10)

# Default max_tokens value for LLM requests - limiting to avoid rate limits
DEFAULT_MAX_TOKENS = 2000

# Default context window management settings
DEFAULT_CHUNK_SIZE = 4000  # Size of chunks for processing large context
DEFAULT_CHUNK_OVERLAP = 200  # Overlap between chunks to maintain context


# --- Models and Enums ---

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class CrewConfig(BaseModel):
    agents_yaml: Dict
    tasks_yaml: Dict
    inputs: Dict
    planning: bool = False
    model: Optional[str] = None
    execution_type: Optional[str] = "crew"  # Added execution_type field with default "crew"

    @property
    def tasks(self) -> Dict:
        """Ensure tasks are properly structured dictionaries"""
        if not isinstance(self.tasks_yaml, dict):
            raise ValueError("Tasks configuration must be a dictionary")
        
        tasks = {}
        for key, value in self.tasks_yaml.items():
            if isinstance(value, str):
                try:
                    tasks[key] = json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Task configuration for {key} is not a valid JSON string")
            else:
                tasks[key] = value
        return tasks

    @property
    def agents(self) -> Dict:
        """Ensure agents are properly structured dictionaries"""
        if not isinstance(self.agents_yaml, dict):
            raise ValueError("Agents configuration must be a dictionary")
        
        agents = {}
        for key, value in self.agents_yaml.items():
            if isinstance(value, str):
                try:
                    agents[key] = json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError(f"Agent configuration for {key} is not a valid JSON string")
            else:
                agents[key] = value
        return agents

    model_config = ConfigDict(arbitrary_types_allowed=True)


class JobBase(BaseModel):
    """Base model with common job fields"""
    job_id: str
    status: str
    created_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    run_name: Optional[str] = None


class JobResponse(BaseModel):
    """Job response model with both JobBase fields and additional fields"""
    job_id: str  # Using individual fields instead of inheritance
    status: str
    created_at: datetime
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    run_name: Optional[str] = None
    # Additional fields
    id: Optional[int] = None
    flow_id: Optional[int] = None
    crew_id: Optional[int] = None
    job_key: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    job_inputs: Optional[Dict[str, Any]] = None
    job_outputs: Optional[Dict[str, Any]] = None
    job_config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


# --- Main job execution function ---

def sanitize_for_database(data: Dict) -> Dict:
    """
    Sanitize task/agent configuration to make it JSON serializable for database storage.
    Removes function objects and other non-serializable elements.
    
    Args:
        data: Dictionary containing configuration data
        
    Returns:
        Dict: A clean, JSON-serializable copy of the data
    """
    if not isinstance(data, dict):
        return data
    
    result = {}
    for key, value in data.items():
        # Skip function objects and other non-serializable types
        if callable(value) or key in ['on_start', 'on_end', 'callback', 'on_task_end']:
            # Store metadata about callbacks instead of the actual functions
            if key == 'callback' and isinstance(value, str):
                result['_callback_name'] = value
            continue
            
        # Handle nested dictionaries
        elif isinstance(value, dict):
            result[key] = sanitize_for_database(value)
        # Handle lists (which might contain dictionaries)
        elif isinstance(value, list):
            result[key] = [
                sanitize_for_database(item) if isinstance(item, dict) else item
                for item in value
            ]
        # Store metadata flags
        elif key.startswith('_'):
            result[key] = value
        # Store serializable values directly
        else:
            try:
                # Test if the value is JSON serializable
                json.dumps(value)
                result[key] = value
            except (TypeError, OverflowError):
                # Skip non-serializable values
                logger_manager.crew.warning(f"Skipping non-serializable value for key {key}")
                continue
    
    return result

async def run_crew_job(job_id: str, config: CrewConfig, db: Session):
    """Set up and run a CrewAI job or Flow."""
    try:
        # Create streaming callback first to capture all logs
        streaming_cb = JobOutputCallback(job_id=job_id, max_retries=3)
        
        logger_manager.crew.info(f"Starting job {job_id}")
        logger_manager.crew.info(f"Received job configuration: {config.dict()}")
        
        # Update status to running
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
        
        # Check execution type
        execution_type = stored_config.get("execution_type", "crew")
        logger_manager.crew.info(f"Execution type: {execution_type}")
        
        # Handle Flow execution
        if execution_type == "flow":
            logger_manager.crew.info(f"Starting Flow execution for job {job_id}")
            
            # We'll need to determine which flow to use
            # For now, this is a placeholder for flow execution
            flow_id = stored_config.get("flow_id")
            
            if not flow_id:
                # If no specific flow ID is provided, try to find a flow in the database
                # For example, by querying the most recent or active flow
                logger_manager.crew.info("No specific flow ID provided, searching for a flow")
                
                # This is a temporary placeholder to find the most recent flow
                # In a real implementation, you would have a more sophisticated way to select the appropriate flow
                flow = db.query(database.Flow).order_by(database.Flow.updated_at.desc()).first()
                
                if flow:
                    flow_id = flow.id
                    logger_manager.crew.info(f"Found most recent flow with ID {flow_id}")
                else:
                    raise Exception("No flow found in the database. Please create a flow first.")
            
            # Create a Backendflow instance
            flow_instance = Backendflow(job_id=job_id, flow_id=flow_id)
            
            try:
                # Direct await the flow kickoff since it's now properly async
                result = await flow_instance.kickoff()
                
                # Update job status based on result
                if result.get("success", False):
                    logger_manager.crew.info(f"Flow job {job_id} completed successfully")
                    jobs[job_id]["status"] = JobStatus.COMPLETED.value
                    jobs[job_id]["result"] = result
                    
                    # Update database
                    db_run.status = JobStatus.COMPLETED.value
                    db_run.result = result
                    db_run.completed_at = datetime.now(UTC)
                    db.commit()
                else:
                    error_msg = result.get("error", "Unknown flow execution error")
                    logger_manager.crew.error(f"Flow job {job_id} failed: {error_msg}")
                    jobs[job_id]["status"] = JobStatus.FAILED.value
                    jobs[job_id]["error"] = error_msg
                    
                    # Update database
                    db_run.status = JobStatus.FAILED.value
                    db_run.error = error_msg
                    db_run.completed_at = datetime.now(UTC)
                    db.commit()
                
                return result
            except Exception as e:
                error_msg = f"Error executing flow: {str(e)}"
                logger_manager.crew.error(error_msg, exc_info=True)
                jobs[job_id]["status"] = JobStatus.FAILED.value
                jobs[job_id]["error"] = error_msg
                
                # Update database
                db_run.status = JobStatus.FAILED.value
                db_run.error = error_msg
                db_run.completed_at = datetime.now(UTC)
                db.commit()
                
                raise Exception(error_msg)
        
        # Regular crew execution (existing code)
        else:
            agents_yaml = stored_config.get("agents_yaml")
            tasks_yaml = stored_config.get("tasks_yaml")
            
            if not agents_yaml or not tasks_yaml:
                raise Exception("Invalid configuration: missing agents or tasks")
            
            # Clean environment for this job
            logger_manager.crew.info(f"Resetting environment for job {job_id}")
            # Reset environment variables
            for key_name in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "DEEPSEEK_API_KEY", "DATABRICKS_TOKEN"]:
                if key_name in os.environ:
                    logger_manager.crew.info(f"Removing {key_name} from environment")
                    os.environ.pop(key_name, None)
            
            # Reset LiteLLM settings through LLMConfig
            LLMConfig.initialize()
                
            # Set the global provider based on the job model, but individual agent calls
            # will use their own provider via the litellm patch
            model = stored_config.get("model")
            if model:
                logger_manager.crew.info(f"Job model is: {model}")
                # Set the detected provider as a reference point, but don't worry too much
                # as the patch will handle provider switching for each API call
                detected_provider = LLMConfig._detect_provider_from_model(model)
                if detected_provider:
                    LLMConfig.set_provider(detected_provider)
                    logger_manager.crew.info(f"Set global provider reference to {detected_provider}")
                
            # Ensure LLMConfig is properly initialized with our provider switching patch
            LLMConfig.initialize()
            
            # Create task status entries for all tasks with initial RUNNING status
            logger_manager.crew.info(f"Creating initial task status entries for job {job_id}")
            create_task_statuses_for_job(db, job_id, tasks_yaml)

            # Ensure each agent has a model specified or use default, and add max_tokens to limit rate limiting
            for agent_key, agent in agents_yaml.items():
                if 'model' not in agent:
                    # Default to GPT-4 if no model specified
                    agent['model'] = "gpt-4"
                
                # Add max_tokens if not specified to avoid rate limiting issues
                if 'max_tokens' not in agent:
                    agent['max_tokens'] = DEFAULT_MAX_TOKENS
                    logger_manager.crew.info(f"Setting max_tokens={DEFAULT_MAX_TOKENS} for agent {agent_key} to avoid rate limiting")
                
                # Add max_rpm if not specified to avoid rate limiting issues
                if 'max_rpm' not in agent:
                    agent['max_rpm'] = 3  # Reasonable default to avoid hitting OpenAI rate limits
                    logger_manager.crew.info(f"Setting max_rpm=3 for agent {agent_key} to avoid rate limiting")
                
                # Ensure respect_context_window is enabled to prevent context overflow
                if 'respect_context_window' not in agent:
                    agent['respect_context_window'] = True
                    logger_manager.crew.info(f"Enabling respect_context_window for agent {agent_key} to avoid context overflow")
                
                # Only override memory/cache settings if explicitly needed to prevent context window issues
                # Check if agent has memory enabled and if we need to override it
                if agent.get('memory', False) == True and 'memory' in agent:
                    logger_manager.crew.info(f"Agent {agent_key} has memory enabled in config, respecting user setting")
                # Otherwise, if not explicitly set or if we're having context window issues, disable it
                else:
                    agent['memory'] = False
                    logger_manager.crew.info(f"Setting memory=False for agent {agent_key} to avoid context overflow")
                
                # Same for cache - respect user setting unless necessary to override
                if agent.get('cache', False) == True and 'cache' in agent:
                    logger_manager.crew.info(f"Agent {agent_key} has cache enabled in config, respecting user setting")
                else:
                    agent['cache'] = False
                    logger_manager.crew.info(f"Setting cache=False for agent {agent_key} to avoid context overflow")
                
                # Configure chunking for handling large contexts
                if 'max_context_window_size' not in agent:
                    # If frontend didn't provide a value, use sensible defaults
                    logger_manager.crew.warning(f"No max_context_window_size provided for agent {agent_key}, using model defaults")
                    if agent['model'] in ["gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "claude-3", "deepseek-v3", "deepseek-coder-v2"]:
                        max_size = 128000  # For newer models with larger context
                    else:
                        max_size = 8192  # Default for most models
                    agent['max_context_window_size'] = max_size
                    logger_manager.crew.info(f"Setting default max_context_window_size={max_size} for agent {agent_key}")
                else:
                    # Log the existing max_context_window_size from frontend
                    logger_manager.crew.info(f"Using frontend-provided max_context_window_size={agent['max_context_window_size']} for agent {agent_key}")
                
                # Add optimizations for managing context window size
                if 'tools' in agent and agent['tools']:
                    logger_manager.crew.info(f"Agent {agent_key} has tools, configuring chunking parameters")
                    # Add chunking parameters to manage tool outputs
                    if 'chunk_size' not in agent:
                        agent['chunk_size'] = DEFAULT_CHUNK_SIZE
                    if 'chunk_overlap' not in agent:
                        agent['chunk_overlap'] = DEFAULT_CHUNK_OVERLAP
                
                logger_manager.crew.info(f"Agent {agent_key} using model: {agent['model']} with max_tokens: {agent['max_tokens']}")

            # Configure callbacks for each task
            for task_key, task in tasks_yaml.items():
                logger_manager.crew.info(f"Configuring task: {task_key}")
                
                # Get agent configuration for this task
                agent_key = task.get('agent')
                if not agent_key or agent_key not in agents_yaml:
                    logger_manager.crew.error(f"Agent '{agent_key}' not found for task '{task_key}'")
                    continue
                    
                agent_config = agents_yaml[agent_key]
                # This function handles task status tracking (running → completed)
                configure_task_callbacks(task_key, task, agent_config, db, job_id)

            # Create sanitized copies of the task and agent configurations for database storage
            sanitized_tasks = {}
            for task_key, task_config in tasks_yaml.items():
                sanitized_tasks[task_key] = sanitize_for_database(task_config)
                
            sanitized_agents = {}
            for agent_key, agent_config in agents_yaml.items():
                sanitized_agents[agent_key] = sanitize_for_database(agent_config)

            # Update stored configuration with sanitized callbacks
            stored_config["tasks_yaml"] = sanitized_tasks
            stored_config["agents_yaml"] = sanitized_agents
            db_run.inputs = stored_config
            db.commit()

            # Initialize the crew instance directly with job_id and configurations
            # Use the unsanitized versions for actual execution
            crew_instance = Backendcrew(job_id=job_id, agents_yaml=agents_yaml, tasks_yaml=tasks_yaml)
            crew = crew_instance.crew()
            
            # Enable verbose callbacks for all crew components
            enable_verbose_callbacks(crew, streaming_cb)
            logger_manager.crew.info("All callbacks and verbose modes configured")

            # Get the current event loop - should be the main application loop
            current_loop = asyncio.get_running_loop()
            
            # Run the actual job in a thread pool to prevent blocking
            try:
                # Use the current loop to schedule the job in a thread pool
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
        logger_manager.crew.error(f"Error running job {job_id}: {str(e)}")
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


# --- API Endpoint Handlers ---

@router.post("")
async def create_job(config: CrewConfig, db: Session = Depends(database.get_db)):
    """Create a new job."""
    try:
        job_id = str(uuid.uuid4())
        
        # Generate a descriptive run name
        model = config.model or "gpt-3.5-turbo"
        run_name = await generate_run_name(config.agents_yaml, config.tasks_yaml, model, db)
        
        # Extract execution type
        execution_type = config.execution_type or "crew"
        
        # Extract flow_id if provided for flow execution
        flow_id = None
        if execution_type == "flow":
            # Try to get flow_id from inputs
            flow_id = config.inputs.get("flow_id")
            
            # If no flow_id is provided, find the most recent flow
            if not flow_id:
                flow = db.query(database.Flow).order_by(database.Flow.updated_at.desc()).first()
                if flow:
                    flow_id = flow.id
                    logger_manager.crew.info(f"Using most recent flow with ID {flow_id}")
                else:
                    raise HTTPException(status_code=400, detail="No flow found in the database. Please create a flow first.")
        
        # Create database entry with all necessary information
        inputs = {
            "agents_yaml": config.agents_yaml,
            "tasks_yaml": config.tasks_yaml,
            "inputs": config.inputs,
            "planning": config.planning,
            "model": config.model,
            "execution_type": execution_type
        }
        
        # Add flow_id to inputs if it exists
        if flow_id:
            inputs["flow_id"] = flow_id
        
        run = database.Run(
            job_id=job_id,
            status=JobStatus.PENDING.value,
            inputs=inputs,
            planning=config.planning,
            run_name=run_name,
            created_at=datetime.now(UTC)
        )
        
        db.add(run)
        db.commit()
        db.refresh(run)
        
        # Add to in-memory storage
        jobs[job_id] = {
            "job_id": job_id,
            "status": JobStatus.PENDING.value,
            "created_at": datetime.now(UTC),
            "run_name": run_name,
            "output": ""
        }
        
        # Launch job asynchronously
        logger_manager.crew.info(f"Created job with ID {job_id}, launching...")
        
        # Use asyncio.create_task to run the job in the background
        asyncio.create_task(run_crew_job(job_id, config, db))
        
        logger_manager.crew.info(f"Job {job_id} launched successfully")
        
        # Return immediately with pending status
        return {
            "job_id": job_id,
            "status": JobStatus.PENDING.value,
            "run_name": run_name
        }
        
    except Exception as e:
        logger_manager.crew.error(f"Error creating job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    """Get the status of a specific job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Include the job_id in the dictionary passed to JobResponse
    job_data = jobs[job_id].copy()
    job_data['job_id'] = job_id
    
    return JobResponse(**job_data)


@router.get("")
async def list_jobs():
    """List all jobs."""
    # Include job_id for each job in the list
    job_list = []
    for job_id, job_data in jobs.items():
        job_with_id = job_data.copy()
        job_with_id['job_id'] = job_id
        job_list.append(JobResponse(**job_with_id))
    
    return job_list


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}