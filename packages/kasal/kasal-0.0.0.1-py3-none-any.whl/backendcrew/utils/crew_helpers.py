"""
Utilities for CrewAI configuration, validation, and setup.
"""
import json
import os
import asyncio
import re
import logging
from typing import Dict, Any, List, Optional, Callable, Union
from datetime import datetime, UTC
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from crewai import Agent, Crew, Task, Process
from crewai.tasks.task_output import TaskOutput

from .. import database
from ..utils.logger_manager import LoggerManager
from ..utils.event_loop import create_and_run_loop, create_task_lifecycle_callback
from ..utils.task_tracker import TaskStatus, update_task_status, create_task_callbacks
from ..callbacks import (
    AgentTraceCallback,
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
)
from ..llm_config import LLMConfig, ModelProvider, SUPPORTED_MODELS
from .api_key_utils import setup_openai_api_key, setup_deepseek_api_key, setup_all_api_keys
from ..tools.tool_factory import ToolFactory
from ..database import SessionLocal

# Initialize logger
logger_manager = LoggerManager()

def is_data_missing(output: TaskOutput) -> bool:
    """Check if we have less than 10 items in the output"""
    logger_manager.crew.info("=== is_data_missing function called ===")
    logger_manager.crew.info(f"TaskOutput type: {type(output)}")
    
    if not hasattr(output, 'pydantic'):
        logger_manager.crew.info("No pydantic model found in output, returning True")
        return True
    
    logger_manager.crew.info(f"Pydantic model: {output.pydantic}")
    logger_manager.crew.info(f"Checking events length in: {output.pydantic.events}")
    events_count = len(output.pydantic.events)
    result = events_count < 10
    
    logger_manager.crew.info(f"Found {events_count} events. Need at least 10.")
    logger_manager.crew.info(f"Is data missing? {result}")
    return result

def validate_model(agent_config: dict) -> bool:
    """Validate if the specified model is supported."""
    model = agent_config.get('model')
    return LLMConfig.validate_model(model)

def create_agent(agent_key: str, agent_config: Dict, config: Dict = None) -> Agent:
    """
    Creates an Agent instance from the provided configuration.
    
    Args:
        agent_key: The unique identifier for the agent
        agent_config: Dictionary containing agent configuration
        config: Global configuration dictionary containing API keys
        
    Returns:
        Agent: A configured CrewAI Agent instance
        
    Raises:
        ValueError: If required fields are missing
    """
    logger_manager.crew.debug(f"Creating agent {agent_key} with config: {agent_config}")
    
    # Validate required fields
    required_fields = ['role', 'goal', 'backstory']
    for field in required_fields:
        if field not in agent_config:
            raise ValueError(f"Missing required field '{field}' in agent configuration")
        if not agent_config[field]:  # Check if field is empty
            raise ValueError(f"Field '{field}' cannot be empty in agent configuration")
    
    # Create tools for this agent
    tools = []
    
    # Process tool ids
    if "tools" in agent_config and agent_config["tools"]:
        tool_ids = agent_config["tools"]
        if isinstance(tool_ids, str):
            # If it's a comma-separated string, split it
            tool_ids = [tid.strip() for tid in tool_ids.split(",") if tid.strip()]
            logger_manager.crew.debug(f"Converted tool_ids from string to list: {tool_ids}")
        
        # Create tools from tool IDs
        # First, check if we have a database config and create a basic tool factory
        db = SessionLocal()
        tool_factory = ToolFactory(config)
        
        for tool_name in tool_ids:
            logger_manager.crew.debug(f"Creating tool: {tool_name}")
            try:
                tool = tool_factory.create_tool(tool_name)
                if tool:
                    tools.append(tool)
                    logger_manager.crew.debug(f"Successfully created and added tool: {tool_name}, tool object: {tool}")
                else:
                    logger_manager.crew.warning(f"Failed to create tool: {tool_name}")
            except Exception as e:
                logger_manager.crew.error(f"Error creating tool {tool_name}: {str(e)}")
        db.close()
        
    logger_manager.crew.debug(f"Final tools list for agent {agent_key}: {tools}")
    
    # Handle LLM configuration
    llm = agent_config.get('llm', LLMConfig.get_default_model())
    
    # CRITICAL: Clean up environment variables to prevent URL conflicts between providers
    import os
    # Clear all API base URLs to prevent conflicts between providers
    for var in ["OPENAI_API_BASE", "ANTHROPIC_API_BASE", "DEEPSEEK_API_BASE", 
                "DATABRICKS_ENDPOINT", "OLLAMA_API_BASE", "OLLAMA_HOST"]:
        if var in os.environ:
            os.environ.pop(var, None)
    
    # Apply LLMConfig's patch to litellm
    import litellm
    LLMConfig.apply_litellm_patch()
    logger_manager.crew.info("Applied LLMConfig patch to litellm")
    
    # Set provider based on the model
    if llm in SUPPORTED_MODELS[ModelProvider.OLLAMA]:
        LLMConfig.set_provider(ModelProvider.OLLAMA)
        logger_manager.crew.info(f"Set provider to Ollama for model: {llm}")
        LLMConfig.setup_ollama_for_agent()
    elif llm in SUPPORTED_MODELS[ModelProvider.OPENAI]:
        LLMConfig.set_provider(ModelProvider.OPENAI)
        logger_manager.crew.info(f"Set provider to OpenAI for model: {llm}")
        LLMConfig.setup_openai_for_agent()
    elif llm in SUPPORTED_MODELS[ModelProvider.DATABRICKS]:
        LLMConfig.set_provider(ModelProvider.DATABRICKS)
        logger_manager.crew.info(f"Set provider to Databricks for model: {llm}")
        LLMConfig.setup_databricks_for_agent()
    elif llm in SUPPORTED_MODELS[ModelProvider.DEEPSEEK]:
        LLMConfig.set_provider(ModelProvider.DEEPSEEK)
        logger_manager.crew.info(f"Set provider to DeepSeek for model: {llm}")
        LLMConfig.setup_deepseek_for_agent()
        
        # Ensure proper environment variables for DeepSeek
        # Clear OpenAI API base completely to prevent conflicts
        os.environ["OPENAI_API_BASE"] = ""
        logger_manager.crew.info("Cleared OPENAI_API_BASE to ensure it doesn't override DeepSeek")
        
        # Force the correct DeepSeek API base URL
        os.environ["DEEPSEEK_API_BASE"] = "https://api.deepseek.com"
        logger_manager.crew.info("Set DEEPSEEK_API_BASE to: https://api.deepseek.com")
        
        # Remove any previously set force completion URL to let LiteLLM handle it
        if "LITELLM_FORCE_COMPLETION_URL" in os.environ:
            os.environ.pop("LITELLM_FORCE_COMPLETION_URL", None)
            logger_manager.crew.info("Removed LITELLM_FORCE_COMPLETION_URL to avoid conflicts")
        
        # Remove any LiteLLM provider setting to ensure it's detected from model name
        if "LITELLM_PROVIDER" in os.environ:
            os.environ.pop("LITELLM_PROVIDER", None)
            logger_manager.crew.info("Removed LITELLM_PROVIDER to ensure detection from model name")
        
        # Make sure the DeepSeek API key is set
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if not api_key:
            logger_manager.crew.warning("DEEPSEEK_API_KEY environment variable not set!")
            # Try to get it from database
            db = SessionLocal()
            from .api_key_utils import setup_provider_api_key
            success = setup_provider_api_key(db, "DEEPSEEK_API_KEY")
            db.close()
            if success:
                logger_manager.crew.info("Successfully set DEEPSEEK_API_KEY from database")
            else:
                logger_manager.crew.error("Failed to set DEEPSEEK_API_KEY from database")
    elif llm in SUPPORTED_MODELS[ModelProvider.ANTHROPIC]:
        LLMConfig.set_provider(ModelProvider.ANTHROPIC)
        logger_manager.crew.info(f"Set provider to Anthropic for model: {llm}")
        LLMConfig.setup_anthropic_for_agent()
        
        # Ensure proper environment variables for Anthropic
        # Anthropic doesn't use OpenAI base URL
        os.environ["OPENAI_API_BASE"] = ""  
        
        # Set the correct Anthropic base URL
        os.environ["ANTHROPIC_API_BASE"] = "https://api.anthropic.com"
        
        # Remove any LiteLLM force URL to let our patched function handle it
        if "LITELLM_FORCE_COMPLETION_URL" in os.environ:
            os.environ.pop("LITELLM_FORCE_COMPLETION_URL", None)
            
        # Make sure ANTHROPIC_API_KEY is set
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            logger_manager.crew.warning("ANTHROPIC_API_KEY environment variable not set!")
            # Try to get it from database via LLMConfig
            db = SessionLocal()
            from .api_key_utils import setup_provider_api_key
            success = setup_provider_api_key(db, "ANTHROPIC_API_KEY")
            db.close()
            if success:
                logger_manager.crew.info("Successfully set ANTHROPIC_API_KEY from database")
            else:
                logger_manager.crew.error("Failed to set ANTHROPIC_API_KEY from database")
    
    # Get the properly formatted model name
    model_name = LLMConfig.get_model_name_for_crewai(llm)
    logger_manager.crew.info(f"Using model: {model_name} for agent {agent_key}")
    
    # Create agent with all available configuration options
    agent_kwargs = {
        'role': agent_config['role'],
        'goal': agent_config['goal'],
        'backstory': agent_config['backstory'],
        'tools': tools,
        'llm': model_name,
        'verbose': agent_config.get('verbose', False),
        'allow_delegation': agent_config.get('allow_delegation', True),
        'cache': agent_config.get('cache', False),
        'allow_code_execution': False,
        'code_execution_mode': 'safe',
        'max_retry_limit': 3,
        'use_system_prompt': True,
        'respect_context_window': True
    }

    # Handle prompt templates
    if 'system_template' in agent_config and agent_config['system_template']:
        agent_kwargs['system_prompt'] = agent_config['system_template']
    if 'prompt_template' in agent_config and agent_config['prompt_template']:
        agent_kwargs['task_prompt'] = agent_config['prompt_template']
    if 'response_template' in agent_config and agent_config['response_template']:
        agent_kwargs['format_prompt'] = agent_config['response_template']

    # Add optional configurations if they exist
    if 'max_iter' in agent_config:
        agent_kwargs['max_iter'] = agent_config.get('max_iter', 15)
    
    # Add max_rpm setting to prevent rate limiting
    if 'max_rpm' in agent_config and agent_config['max_rpm'] is not None:
        agent_kwargs['max_rpm'] = agent_config['max_rpm']
        logger_manager.crew.info(f"Setting max_rpm={agent_config['max_rpm']} for agent {agent_key}")
    else:
        # For Anthropic models, set a safe default RPM if not specified
        if model_name and any(model_type in model_name.lower() for model_type in ['claude']):
            agent_kwargs['max_rpm'] = 3  # Default to 3 RPM for Anthropic models
            logger_manager.crew.info(f"Setting default max_rpm=3 for Anthropic model {model_name}")
    
    # Set max_tokens for the agent to avoid rate limiting
    if 'max_tokens' in agent_config and agent_config['max_tokens'] is not None:
        agent_kwargs['max_tokens'] = agent_config['max_tokens']
        logger_manager.crew.info(f"Setting max_tokens={agent_config['max_tokens']} for agent {agent_key}")
    
    # Respect context window setting to avoid overflow
    if 'respect_context_window' in agent_config:
        agent_kwargs['respect_context_window'] = agent_config['respect_context_window']
        logger_manager.crew.info(f"Setting respect_context_window={agent_config['respect_context_window']} for agent {agent_key}")
    
    # Set memory setting from config or default to False if not specified
    if 'memory' in agent_config:
        agent_kwargs['memory'] = agent_config.get('memory', False)
        logger_manager.crew.info(f"Setting memory={agent_config.get('memory', False)} for agent {agent_key}")
    
    # Set cache setting from config or default to False if not specified
    if 'cache' in agent_config:
        agent_kwargs['cache'] = agent_config.get('cache', False)
        logger_manager.crew.info(f"Setting cache={agent_config.get('cache', False)} for agent {agent_key}")
    
    logger_manager.crew.info(f"Memory/cache settings for agent {agent_key}: memory={agent_kwargs.get('memory', False)}, cache={agent_kwargs['cache']}")
    
    # Configure context window size
    if 'max_context_window_size' in agent_config:
        agent_kwargs['max_context_window_size'] = agent_config['max_context_window_size']
        logger_manager.crew.info(f"Using frontend-provided max_context_window_size={agent_config['max_context_window_size']} for agent {agent_key}")
    else:
        # Auto-detect best context window size for known models with larger context windows
        logger_manager.crew.warning(f"No max_context_window_size provided for agent {agent_key}, detecting from model")
        # More comprehensive model detection with better coverage of recent models
        large_context_models = [
            # OpenAI large context models
            'gpt-4-turbo', 'gpt-4o', 'gpt-4-32k', 'gpt-4o-mini', 
            # Anthropic large context models
            'claude-3', 'claude-3-5', 'claude-3-7', 'claude-3-opus', 'claude-3-5-sonnet', 'claude-3-5-haiku',
            # DeepSeek large context models
            'deepseek-v3', 'deepseek-coder-v2', 'deepseek-chat', 'deepseek-reasoner',
            # Meta/Llama large context models
            'llama3.2', 'llama3:latest', 'databricks-meta-llama-3', 
            # Qwen large context models
            'qwen2.5'
        ]
        
        if model_name and any(model_type in model_name.lower() for model_type in large_context_models):
            agent_kwargs['max_context_window_size'] = 128000
            logger_manager.crew.info(f"Auto-detected large context model: {model_name}, setting max_context_window_size=128000")
        else:
            # Default context window size for other models
            agent_kwargs['max_context_window_size'] = 8192
            logger_manager.crew.info(f"Using default max_context_window_size=8192 for model: {model_name}")
    
    # Configure chunking for large content
    if 'chunk_size' in agent_config:
        agent_kwargs['chunk_size'] = agent_config['chunk_size']
        logger_manager.crew.info(f"Setting chunk_size={agent_config['chunk_size']} for agent {agent_key}")
    
    if 'chunk_overlap' in agent_config:
        agent_kwargs['chunk_overlap'] = agent_config['chunk_overlap']
        logger_manager.crew.info(f"Setting chunk_overlap={agent_config['chunk_overlap']} for agent {agent_key}")
    
    if 'max_execution_time' in agent_config:
        agent_kwargs['max_execution_time'] = agent_config.get('max_execution_time')
    if 'function_calling_llm' in agent_config:
        agent_kwargs['function_calling_llm'] = agent_config.get('function_calling_llm')

    agent = Agent(**agent_kwargs)
    logger_manager.crew.debug(f"Created agent {agent_key}: {agent}")
    return agent

def create_task(task_key: str, task_config: dict, agent: Agent, output_dir: Optional[str] = None, config: dict = None) -> Task:
    """
    Creates a Task instance from the provided configuration.
    
    Args:
        task_key: The unique identifier for the task
        task_config: Dictionary containing task configuration
        agent: The agent that will perform this task
        output_dir: Optional directory for output files
        config: Global configuration dictionary containing API keys
        
    Returns:
        Task: A configured CrewAI Task instance
    """
    from ..tools.tool_schemas import TOOL_OUTPUT_MODELS
    from pathlib import Path

    logger_manager.crew.debug(f"Creating task: {task_key} with config: {task_config}")
    logger_manager.crew.debug(f"Using agent: {agent}")
    
    # Initialize base task arguments
    task_args = {
        'description': task_config['description'],
        'expected_output': task_config['expected_output'],
        'agent': agent,
        'name': task_key
    }
    
    # Handle tools if specified in task config
    if 'tools' in task_config and config:
        tools = []
        tool_factory = ToolFactory(config)
        
        for tool_name in task_config['tools']:
            tool = tool_factory.create_tool(tool_name)
            if tool:
                tools.append(tool)
                logger_manager.crew.info(f"Added tool: {tool_name} to task: {task_key}")
            else:
                logger_manager.crew.warning(f"Skipped unavailable tool: {tool_name} for task: {task_key}")
        
        task_args['tools'] = tools

    # Pass through any callback that was set in the task config
    if 'callback' in task_config:
        task_args['callback'] = task_config['callback']

    # Add output file for tasks that need it
    if output_dir and task_key == 'reporting_task':
            report_path = str(Path(output_dir) / "report.md")
            logger_manager.crew.info(f"Using report path: {report_path}")
            task_args['output_file'] = report_path
    
    # Handle other optional task configurations
    optional_fields = [
        'async_execution',
        'context_tasks',
        'human_input',
        'converter_cls'
    ]
    
    # Handle output configurations separately
    if 'output_json' in task_config:
        # If output_json is 'false' or False, don't include it in task_args
        if not (isinstance(task_config['output_json'], str) and task_config['output_json'].lower() == 'false'):
            task_args['output_json'] = task_config['output_json']
    
    if 'output_pydantic' in task_config and task_config['output_pydantic']:
        model_name = task_config['output_pydantic']
        if isinstance(model_name, str):
            # Get the model class directly from TOOL_OUTPUT_MODELS
            model_class = TOOL_OUTPUT_MODELS.get(model_name)
            if model_class:
                task_args['output_pydantic'] = model_class
            else:
                logger_manager.crew.warning(f"Unknown output_pydantic model: {model_name}, setting to None")
                task_args['output_pydantic'] = None
        else:
            task_args['output_pydantic'] = task_config['output_pydantic']
    
    for field in optional_fields:
        if field in task_config:
            task_args[field] = task_config[field]

    return Task(**task_args)

def setup_api_key(db: Session) -> None:
    """Set up the API keys from the database using LLMConfig."""
    # Use API key utility functions from LLMConfig
    LLMConfig.setup_openai_for_agent()
    LLMConfig.setup_anthropic_for_agent()
    LLMConfig.setup_deepseek_for_agent()
    LLMConfig.setup_databricks_for_agent()
    LLMConfig.setup_ollama_for_agent()
    logger_manager.crew.info("Set up all API keys using LLMConfig")

def configure_process_output_handler(job_callback) -> callable:
    """Create a process output handler that captures stdout."""
    def process_output(output):
        try:
            # Always send the output through the callback
            job_callback(output)
            # Print to stdout to ensure it's captured
            print(str(output))
            return output
        except Exception as e:
            logger_manager.crew.error(f"Error in process output handler: {e}", exc_info=True)
            return output
    return process_output

def configure_task_callbacks(task_key: str, task: dict, agent_config: dict, db: Session, job_id: str) -> None:
    """Configure callbacks for a task."""
    # Get retry configuration from agent's max_iter
    max_retries = agent_config.get('max_iter', 3)
    retry_delay = task.get('retry_delay', 1)  # seconds
    
    logger_manager.crew.info(f"Using agent max_iter={max_retries} for task '{task_key}' retries")
    
    # Initialize a list to store all callbacks
    callbacks = []
    
    # Add the agent callback for database tracking
    agent_cb = AgentTraceCallback(
        db=db,
        job_id=job_id,
        max_retries=max_retries,
        task_key=task_key
    )
    callbacks.append(agent_cb)
    
    # Add task-specific callback if it exists
    task_callback = task.get('callback')
    if task_callback:
        logger_manager.crew.info(f"Task {task_key} has task-specific callback: {task_callback}")
        
        if isinstance(task_callback, str):
            try:
                callback_map = {
                    'TaskCompletionLogger': TaskCompletionLogger,
                    'DetailedOutputLogger': DetailedOutputLogger,
                    'SchemaValidator': SchemaValidator,
                    'ContentValidator': ContentValidator,
                    'TypeValidator': TypeValidator,
                    'JsonFileStorage': JsonFileStorage,
                    'DatabaseStorage': DatabaseStorage,
                    'FileSystemStorage': FileSystemStorage,
                    'OutputFormatter': OutputFormatter,
                    'DataExtractor': DataExtractor,
                    'OutputEnricher': OutputEnricher,
                    'OutputSummarizer': OutputSummarizer,
                    'AgentTraceCallback': AgentTraceCallback
                }
                
                if task_callback in callback_map:
                    callback_class = callback_map[task_callback]
                    # Handle special case for AgentTraceCallback
                    if callback_class == AgentTraceCallback:
                        callback_instance = callback_class(
                            db=db,
                            job_id=job_id,
                            max_retries=max_retries,
                            task_key=task_key
                        )
                    else:
                        callback_instance = callback_class(
                            max_retries=max_retries,
                            task_key=task_key
                        )
                    logger_manager.crew.info(f"Created callback '{task_callback}' with max_retries={max_retries}")
                    callbacks.append(callback_instance)
                else:
                    logger_manager.crew.warning(f"Callback '{task_callback}' not found in available callbacks")
            except Exception as e:
                logger_manager.crew.error(f"Error creating callback '{task_callback}': {e}")
                logger_manager.crew.error("Stack trace:", exc_info=True)
        elif callable(task_callback):
            # Create a simple async wrapper for callable callbacks
            async def async_wrapper(output):
                return task_callback(output)
            callbacks.append(async_wrapper)
    
    # Add a status tracking callback to update task status
    async def status_tracking_callback(output):
        try:
            # Update task status to completed when done
            update_task_status(db, job_id, task_key, TaskStatus.COMPLETED)
            logger_manager.crew.info(f"Task {task_key} marked as completed")
            return output
        except Exception as e:
            logger_manager.crew.error(f"Error updating task status: {str(e)}")
            return output
    
    callbacks.append(status_tracking_callback)
    
    # Create a combined callback that executes all callbacks in sequence
    async def combined_callback(output):
        results = []
        for callback in callbacks:
            try:
                result = await callback(output)
                results.append(result)
            except Exception as e:
                logger_manager.crew.error(f"Callback failed for task '{task_key}': {e}")
                # Store failure information
                db_run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
                if db_run:
                    error_trace = database.ErrorTrace(
                        run_id=db_run.id,
                        task_key=task_key,
                        error_type="callback_failure",
                        error_message=str(e),
                        timestamp=datetime.now(UTC),
                        error_metadata={
                            'callback_name': getattr(e, 'callback_name', 'unknown'),
                            'retry_count': getattr(e, 'retry_count', 0),
                            'error': str(e)
                        }
                    )
                    db.add(error_trace)
                    db.commit()
                
                # Update task status to failed on error
                try:
                    update_task_status(db, job_id, task_key, TaskStatus.FAILED)
                    logger_manager.crew.info(f"Task {task_key} marked as failed due to callback error")
                except Exception as update_error:
                    logger_manager.crew.error(f"Error updating task status to failed: {str(update_error)}")
                    
                # Re-raise to trigger task retry
                raise
        return results
    
    # Create a sync wrapper for the async callback using our event loop utility
    def sync_callback(output):
        return create_and_run_loop(combined_callback(output))
    
    # Store the original callback name (if it's a string) for database serialization
    if isinstance(task.get('callback'), str):
        task['_callback_name'] = task['callback']
    
    # Create task status callbacks using the helper function
    status_callbacks = create_task_callbacks(db, job_id, task_key)
    
    # Make a runtime-only copy of the task with callbacks
    # This copy is used for actual execution but not stored in the database
    runtime_task = task.copy()
    
    # Set the sync callback for CrewAI runtime execution
    runtime_task['callback'] = sync_callback
    
    # Create specific lifecycle hooks for task start and end events for runtime
    # The status transitions handled are: 
    # - On start: set/confirm status as RUNNING
    # - On end: update status to COMPLETED
    # - On error: update status to FAILED
    runtime_task['on_start'] = status_callbacks['on_start']
    runtime_task['on_end'] = status_callbacks['on_end']
    runtime_task['on_task_end'] = sync_callback
    
    # Configure retry behavior in both original task and runtime task
    task['retry_on_fail'] = True
    task['max_retries'] = max_retries
    task['retry_delay'] = retry_delay
    runtime_task['retry_on_fail'] = True
    runtime_task['max_retries'] = max_retries
    runtime_task['retry_delay'] = retry_delay
    
    # Add task metadata to both versions
    if 'name' not in task:
        task['name'] = task_key
        runtime_task['name'] = task_key
    if 'description' not in task:
        task['description'] = f"Task {task_key}"
        runtime_task['description'] = f"Task {task_key}"
    
    # Special handling for on_start and on_end in the task dictionary
    # Store a flag that these lifecycle hooks will be added at runtime
    task['_has_status_tracking'] = True
    
    # Update the original task reference with the runtime task for execution
    # but not for database storage
    for key, value in runtime_task.items():
        if not key.startswith('_'):  # Skip metadata fields
            task[key] = value
    
    logger_manager.crew.info(f"Updated task {task_key} with {len(callbacks)} callbacks")

def enable_verbose_callbacks(crew: Crew, streaming_cb) -> None:
    """Enable verbose mode and callbacks for the crew and all its components."""
    # Enable verbose mode and set callback for crew process
    crew.process.verbose = True
    crew.process.output_callback = streaming_cb.execute
    logger_manager.crew.info("Enabled verbose output for crew process")
    
    # Enable verbose mode and callbacks for all tasks and agents
    for task in crew.tasks:
        # Enable verbose mode and callback for task process
        if hasattr(task, 'process'):
            task.process.verbose = True
            task.process.output_callback = streaming_cb.execute
            logger_manager.crew.info(f"Enabled verbose output for task: {task.description}")
        
        # Enable verbose mode and callback for agent process
        if hasattr(task, 'agent'):
            agent = task.agent
            if hasattr(agent, 'process'):
                agent.process.verbose = True
                agent.process.output_callback = streaming_cb.execute
                logger_manager.crew.info(f"Enabled verbose for agent in task: {task.description}")
            
            # Enable verbose mode and callback for tool processes
            if hasattr(agent, 'tools'):
                for tool in agent.tools:
                    if hasattr(tool, 'process'):
                        tool.process.verbose = True
                        tool.process.output_callback = streaming_cb.execute
                        logger_manager.crew.info(f"Enabled verbose for tool in task: {task.description}")

async def convert_tool_ids(config_obj: Any, db: Session) -> None:
    """Convert tool IDs to tool names in agents and tasks configuration."""
    # Get all tools from database for lookup
    tools = db.query(database.Tool).all()
    tools_lookup = {tool.id: tool.title for tool in tools}
    
    # Convert tool IDs to names in agents configuration
    for agent_key, agent in config_obj.agents_yaml.items():
        if 'tools' in agent and agent['tools']:
            agent['tools'] = [
                tools_lookup[tool_id] if isinstance(tool_id, int) and tool_id in tools_lookup 
                else tools_lookup.get(int(tool_id)) if isinstance(tool_id, str) and tool_id.isdigit() 
                else tool_id
                for tool_id in agent['tools']
            ]
            logger_manager.crew.info(f"Converted tools for agent {agent_key}: {agent['tools']}")
    
    # Convert tool IDs to names in tasks configuration
    for task_key, task in config_obj.tasks_yaml.items():
        if 'tools' in task and task['tools']:
            task['tools'] = [
                tools_lookup[tool_id] if isinstance(tool_id, int) and tool_id in tools_lookup 
                else tools_lookup.get(int(tool_id)) if isinstance(tool_id, str) and tool_id.isdigit() 
                else tool_id
                for tool_id in task['tools']
            ]
            logger_manager.crew.info(f"Converted tools for task {task_key}: {task['tools']}")

def order_tasks_by_dependencies(tasks_yaml: Dict) -> Dict:
    """Order tasks based on their dependencies."""
    ordered_tasks = {}
    processed_tasks = set()
    
    def add_task_with_dependencies(t_key):
        if t_key in processed_tasks:
            return
        t = tasks_yaml[t_key]
        # Add context tasks first
        for context_task in t.get('context', []):
            if context_task in tasks_yaml:
                add_task_with_dependencies(context_task)
        ordered_tasks[t_key] = t
        processed_tasks.add(t_key)
    
    # Process all tasks to ensure proper ordering
    for t_key in tasks_yaml:
        add_task_with_dependencies(t_key)
    
    return ordered_tasks

def validate_tasks_and_agents(ordered_tasks: Dict, agents_yaml: Dict) -> None:
    """Validate task dependencies and agent references."""
    for task_key, task in ordered_tasks.items():
        if task.get('context'):
            for context_task in task['context']:
                if context_task not in ordered_tasks:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Context task '{context_task}' referenced in task '{task_key}' not found"
                    )
        
        # Ensure each task has a valid agent
        agent_name = task.get('agent')
        if not agent_name or agent_name not in agents_yaml:
            raise HTTPException(
                status_code=400,
                detail=f"Agent '{agent_name}' referenced in task '{task_key}' not found"
            ) 