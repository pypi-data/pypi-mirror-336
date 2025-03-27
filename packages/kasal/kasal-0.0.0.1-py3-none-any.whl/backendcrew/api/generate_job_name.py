from typing import Dict
import logging
import litellm
import sys
import traceback
import os
from datetime import datetime
from sqlalchemy.orm import Session
from ..llm_config import LLMConfig, ModelProvider
from ..utils.model_config import get_model_config
from ..utils.crew_helpers import setup_api_key
# Import BAML components - using baml_py which we know is installed
from baml_py import BamlRuntime
from baml_py.baml_py import ClientRegistry

logger = logging.getLogger(__name__)

# Define BAML function inline for minimal change
BAML_GENERATE_NAME_FUNCTION = """
function GenerateRunName(jobSummary: string) -> string {
  client default
  prompt #"
    Generate a concise, descriptive name (2-4 words) for an AI job run based on the agents and tasks involved.
    Focus on the specific domain, region, and purpose of the job.
    The name should reflect the main activity (e.g., 'Lebanese News Monitor' for a Lebanese journalist monitoring news).
    Prioritize including:
    1. The region or topic (e.g., Lebanese, Beirut)
    2. The main activity (e.g., News Analysis, Press Review)
    Only return the name, no explanations or additional text.
    Avoid generic terms like 'Agent', 'Task', 'Initiative', or 'Collaboration'.

    Job details:
    {{ jobSummary }}
  "#
}
"""

async def generate_run_name(agents_yaml: Dict, tasks_yaml: Dict, model: str, db: Session = None) -> str:
    """
    Generate a descriptive run name based on the agents and tasks configuration.
    Returns a 2-4 word descriptive name.
    """
    try:
        logger.info(f"Generating run name using model: {model}")
        
        # Set up API key from database if db session is provided
        if db:
            # This function retrieves encrypted keys from DB, decrypts them,
            # and sets up environment variables with the decrypted keys
            setup_api_key(db)
            logger.info("API key setup completed")
        else:
            logger.warning("No DB connection provided for API key setup")

        # Create a summary of the job for the LLM
        job_summary = f"""Agent Details:"""
        for agent_key, agent in agents_yaml.items():
            job_summary += f"""
Role: {agent.get('role', '')}
Goal: {agent.get('goal', '')}
Backstory: {agent.get('backstory', '')}"""

        job_summary += "\n\nTasks:"
        for task_key, task in tasks_yaml.items():
            job_summary += f"""
Description: {task.get('description', '')}
Expected Output: {task.get('expected_output', '')}"""
        
        # Get model config for logging
        model_config = get_model_config(model)
        logger.info(f"Using model: {model}, provider: {model_config['provider']}")
        
        # Prepare the messages array for LLMConfig
        system_message = """Generate a concise, descriptive name (2-4 words) for an AI job run based on the agents and tasks involved.
Focus on the specific domain, region, and purpose of the job.
The name should reflect the main activity (e.g., 'Lebanese News Monitor' for a Lebanese journalist monitoring news).
Prioritize including:
1. The region or topic (e.g., Lebanese, Beirut)
2. The main activity (e.g., News Analysis, Press Review)
Only return the name, no explanations or additional text.
Avoid generic terms like 'Agent', 'Task', 'Initiative', or 'Collaboration'."""

        # Prepare the messages array
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": job_summary}
        ]
        
        try:
            # Let LLMConfig handle all model-specific configuration
            response = await LLMConfig.generate_async_completion(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=20,
                db=db
            )
            
            # Extract the name from the response
            run_name = response["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated run name: {run_name}")
            return run_name
            
        except Exception as completion_error:
            logger.error(f"Error in LLMConfig.generate_async_completion: {str(completion_error)}")
            logger.error(f"With model: {model}, provider: {model_config['provider']}")
            # Re-raise to be caught by outer exception handler
            raise

    except Exception as e:
        logger.error(f"Error generating run name: {str(e)}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logger.error("Exception traceback:")
        for line in tb_lines:
            logger.error(line.rstrip())
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"Job-{timestamp}" 