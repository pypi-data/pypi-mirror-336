from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import json
import logging
import os
import traceback
from ..database import get_async_db
from ..utils.openai_utils import get_openai_client
from datetime import datetime
from ..database import LLMLog
from os import getenv
from ..utils.model_config import get_model_config
from ..utils.crew_helpers import setup_api_key
# Import utilities for direct API calls
import aiohttp
import requests

# Import key management utilities directly
from ..utils.api_key_utils import async_setup_openai_api_key, async_setup_anthropic_api_key, async_setup_deepseek_api_key, async_setup_all_api_keys

router = APIRouter()
logger = logging.getLogger(__name__)

# Define system prompt for agent-task connection generation
CONNECTIONS_SYSTEM_PROMPT = """You are an expert at analyzing AI agents and tasks to create optimal connections.
Given one or more agents and tasks, suggest the best assignments ensuring:
1. Every agent has at least one task
2. Tasks are assigned based on agent capabilities and expertise
3. Tasks should follow a logical workflow sequence
4. One agent can handle multiple tasks if their skills align

IMPORTANT: When determining dependencies, consider:
- What information or output is needed from other tasks
- The natural sequence of work (e.g., research → analysis → presentation)
- Dependencies should reflect the logical flow of information
- Each task should wait for prerequisite tasks that provide necessary inputs

CRITICAL OUTPUT INSTRUCTIONS:
1. Return ONLY raw JSON without any markdown formatting or code block markers
2. Do not include ```json, ``` or any other markdown syntax
3. The response must be a single JSON object that can be directly parsed

Expected JSON structure:
{
    "assignments": [
        {
            "agent_name": "agent name",
            "tasks": [
                {
                    "task_name": "task name",
                    "reasoning": "brief explanation of why this task fits this agent"
                }
            ]
        }
    ],
    "dependencies": [
        {
            "task_name": "task name",
            "required_before": ["task names that must be completed first"],
            "reasoning": "explain why these tasks must be completed first and how their output is used"
        }
    ]
}

Only include tasks in the dependencies array if they actually have prerequisites.
Think carefully about the workflow and how information flows between tasks."""

class ConnectionRequest(BaseModel):
    agents: list[dict]
    tasks: list[dict]
    model: str = "gpt-4-turbo"

# Add helper function for logging LLM interactions
async def log_llm_interaction(db: AsyncSession, endpoint: str, prompt: str, response: str, model: str, status: str = 'success', error_message: str = None):
    """Log LLM interaction to database"""
    try:
        llm_log = LLMLog(
            endpoint=endpoint,
            prompt=prompt,
            response=response,
            model=model,
            status=status,
            error_message=error_message,
            created_at=datetime.utcnow()
        )
        db.add(llm_log)
        await db.commit()
        logger.info(f"Logged {endpoint} interaction to database")
    except Exception as e:
        logger.error(f"Failed to log LLM interaction: {str(e)}")
        await db.rollback()

# Add a helper function to validate OpenAI API key
async def validate_openai_api_key(api_key):
    """Test OpenAI API key by making a simple models list request"""
    if not api_key:
        return False, "No API key provided"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Just test listing models which is a lightweight call
            async with session.get("https://api.openai.com/v1/models", headers=headers) as response:
                if response.status == 200:
                    return True, "API key is valid"
                else:
                    error_text = await response.text()
                    return False, f"API key validation failed: {response.status} - {error_text}"
    except Exception as e:
        return False, f"API key validation error: {str(e)}"

@router.get("/test-api-key")
async def test_api_key():
    """Test endpoint to validate API keys and configuration"""
    results = {}
    
    # Test OpenAI API key
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        valid, message = await validate_openai_api_key(openai_key)
        results["openai"] = {
            "has_key": True,
            "valid": valid,
            "message": message,
            "key_prefix": openai_key[:4] + "..." if openai_key else "None"
        }
    else:
        results["openai"] = {
            "has_key": False,
            "valid": False,
            "message": "No API key found in environment variables"
        }
    
    # Test Anthropic API key (simple presence check)
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    results["anthropic"] = {
        "has_key": bool(anthropic_key),
        "key_prefix": anthropic_key[:4] + "..." if anthropic_key else "None"
    }
    
    # Test DeepSeek API key (simple presence check)
    deepseek_key = os.environ.get('DEEPSEEK_API_KEY')
    results["deepseek"] = {
        "has_key": bool(deepseek_key),
        "key_prefix": deepseek_key[:4] + "..." if deepseek_key else "None"
    }
    
    # Also include Python version info as this might be relevant
    import sys
    results["python_info"] = {
        "version": sys.version,
        "executable": sys.executable,
        "platform": sys.platform
    }
        
    return results

@router.post("/generate-connections")
async def generate_connections(request: ConnectionRequest, db: AsyncSession = Depends(get_async_db)):
    try:
        model_config = get_model_config(request.model)
        
        # Format agents and tasks for the prompt
        agents_info = "AVAILABLE AGENTS:\n"
        for idx, agent in enumerate(request.agents, 1):
            agents_info += f"\n{idx}. Agent: {agent['name']}\n"
            agents_info += f"   Role: {agent['role']}\n"
            agents_info += f"   Goal: {agent['goal']}\n"
            agents_info += f"   Background: {agent.get('backstory', 'Not provided')}\n"
            if agent.get('tools'):
                agents_info += f"   Tools: {', '.join(agent['tools'])}\n"

        tasks_info = "TASKS TO ASSIGN:\n"
        for idx, task in enumerate(request.tasks, 1):
            tasks_info += f"\n{idx}. Task: {task['name']}\n"
            tasks_info += f"   Description: {task['description']}\n"
            if task.get('expected_output'):
                tasks_info += f"   Expected Output: {task['expected_output']}\n"
            if task.get('tools'):
                tasks_info += f"   Required Tools: {', '.join(task['tools'])}\n"
            if task.get('context'):
                context = task['context']
                tasks_info += f"   Type: {context.get('type', 'general')}\n"
                tasks_info += f"   Priority: {context.get('priority', 'medium')}\n"
                tasks_info += f"   Complexity: {context.get('complexity', 'medium')}\n"
                if context.get('required_skills'):
                    tasks_info += f"   Required Skills: {', '.join(context['required_skills'])}\n"
            
        # Create prompt for logging immediately
        prompt_for_log = f"Agents: {agents_info}\nTasks: {tasks_info}"

        # Set up provider-specific configurations using the LLMConfig helper classes
        provider = model_config['provider'].lower()
        
        # Setup API keys based on the provider
        if provider == 'openai':
            from ..llm_config import LLMConfig
            LLMConfig.setup_openai_for_agent()
            logger.info("Set up OpenAI configuration for agent")
        elif provider == 'anthropic':
            from ..llm_config import LLMConfig
            LLMConfig.setup_anthropic_for_agent()
            logger.info("Set up Anthropic configuration for agent")
        elif provider == 'deepseek':
            from ..llm_config import LLMConfig
            LLMConfig.setup_deepseek_for_agent()
            logger.info("Set up DeepSeek configuration for agent")
        else:
            # Fallback: set up all keys
            await async_setup_all_api_keys(db)
            logger.info(f"Used generic key setup for provider: {provider}")
            
        # Get API key based on provider
        api_key_env_var = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY'
        }.get(provider, 'OPENAI_API_KEY')
        
        api_key = os.environ.get(api_key_env_var)
        if not api_key:
            error_msg = f"No API key found for provider: {provider}"
            logger.error(error_msg)
            await log_llm_interaction(
                db=db,
                endpoint='generate-connections',
                prompt=prompt_for_log,
                response="Error: No API key found",
                model=request.model,
                status='error',
                error_message=error_msg
            )
            raise HTTPException(status_code=500, detail=error_msg)
        
        logger.info(f"Using {provider} API key: {api_key[:4]}...")
        
        # The user content stays the same regardless of the provider
        user_content = f"""Available Agents:
{agents_info}

Tasks to Assign:
{tasks_info}"""
        
        content = None
        try:
            # OpenAI API call
            if provider.lower() == 'openai':
                try:
                    import openai
                    
                    # Setup OpenAI client
                    client = openai.OpenAI(api_key=api_key)
                    
                    # Make API call
                    response = client.chat.completions.create(
                        model=request.model,
                        messages=[
                            {"role": "system", "content": CONNECTIONS_SYSTEM_PROMPT},
                            {"role": "user", "content": user_content}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    
                    content = response.choices[0].message.content
                    logger.info(f"Successfully received OpenAI API response (first 100 chars): {content[:100]}")
                    
                except Exception as e:
                    error_msg = f"OpenAI API error: {str(e)}"
                    logger.error(error_msg)
                    await log_llm_interaction(
                        db=db,
                        endpoint='generate-connections',
                        prompt=prompt_for_log,
                        response="Error: OpenAI API call failed",
                        model=request.model,
                        status='error',
                        error_message=error_msg
                    )
                    raise HTTPException(status_code=500, detail=error_msg)
            
            # Anthropic API call
            elif provider.lower() == 'anthropic':
                try:
                    import anthropic
                    
                    # Setup Anthropic client
                    client = anthropic.Anthropic(api_key=api_key)
                    
                    # Make API call
                    response = client.messages.create(
                        model=request.model,
                        max_tokens=2000,
                        messages=[
                            {"role": "user", "content": f"{CONNECTIONS_SYSTEM_PROMPT}\n\n{user_content}"}
                        ]
                    )
                    
                    content = response.content[0].text
                    logger.info(f"Successfully received Anthropic API response (first 100 chars): {content[:100]}")
                    
                except Exception as e:
                    error_msg = f"Anthropic API error: {str(e)}"
                    logger.error(error_msg)
                    await log_llm_interaction(
                        db=db,
                        endpoint='generate-connections',
                        prompt=prompt_for_log,
                        response="Error: Anthropic API call failed",
                        model=request.model,
                        status='error',
                        error_message=error_msg
                    )
                    raise HTTPException(status_code=500, detail=error_msg)
            
            # DeepSeek API call
            elif provider.lower() == 'deepseek':
                try:
                    import requests
                    
                    # Make API call
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": request.model,
                            "messages": [
                                {"role": "system", "content": CONNECTIONS_SYSTEM_PROMPT},
                                {"role": "user", "content": user_content}
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2000
                        }
                    )
                    
                    if response.status_code != 200:
                        error_msg = f"DeepSeek API error: {response.text}"
                        logger.error(error_msg)
                        await log_llm_interaction(
                            db=db,
                            endpoint='generate-connections',
                            prompt=prompt_for_log,
                            response="Error: DeepSeek API call failed",
                            model=request.model,
                            status='error',
                            error_message=error_msg
                        )
                        raise HTTPException(status_code=500, detail=error_msg)
                    
                    content = response.json()["choices"][0]["message"]["content"]
                    logger.info(f"Successfully received DeepSeek API response (first 100 chars): {content[:100]}")
                    
                except Exception as e:
                    error_msg = f"DeepSeek API error: {str(e)}"
                    logger.error(error_msg)
                    await log_llm_interaction(
                        db=db,
                        endpoint='generate-connections',
                        prompt=prompt_for_log,
                        response="Error: DeepSeek API call failed",
                        model=request.model,
                        status='error',
                        error_message=error_msg
                    )
                    raise HTTPException(status_code=500, detail=error_msg)
            
            if not content:
                error_msg = "No response content received from API"
                logger.error(error_msg)
                await log_llm_interaction(
                    db=db,
                    endpoint='generate-connections',
                    prompt=prompt_for_log,
                    response="Error: No response content",
                    model=request.model,
                    status='error',
                    error_message=error_msg
                )
                raise HTTPException(status_code=500, detail=error_msg)
            
            # Parse the response
            try:
                response_data = json.loads(content)
                
                # Validate the response structure
                if not isinstance(response_data, dict) or 'assignments' not in response_data or 'dependencies' not in response_data:
                    error_msg = "Invalid response structure from API"
                    logger.error(error_msg)
                    await log_llm_interaction(
                        db=db,
                        endpoint='generate-connections',
                        prompt=prompt_for_log,
                        response=content,
                        model=request.model,
                        status='error',
                        error_message=error_msg
                    )
                    raise HTTPException(status_code=500, detail=error_msg)
                
                # Validate assignments
                assigned_tasks = set()
                for assignment in response_data['assignments']:
                    if not isinstance(assignment, dict) or 'agent_name' not in assignment or 'tasks' not in assignment:
                        error_msg = "Invalid assignment structure in response"
                        logger.error(error_msg)
                        await log_llm_interaction(
                            db=db,
                            endpoint='generate-connections',
                            prompt=prompt_for_log,
                            response=content,
                            model=request.model,
                            status='error',
                            error_message=error_msg
                        )
                        raise HTTPException(status_code=500, detail=error_msg)
                    
                    for task in assignment['tasks']:
                        if not isinstance(task, dict) or 'task_name' not in task or 'reasoning' not in task:
                            error_msg = "Invalid task structure in assignment"
                            logger.error(error_msg)
                            await log_llm_interaction(
                                db=db,
                                endpoint='generate-connections',
                                prompt=prompt_for_log,
                                response=content,
                                model=request.model,
                                status='error',
                                error_message=error_msg
                            )
                            raise HTTPException(status_code=500, detail=error_msg)
                        
                        assigned_tasks.add(task['task_name'])
                
                # Check for unassigned tasks
                all_tasks = {task['name'] for task in request.tasks}
                unassigned_tasks = all_tasks - assigned_tasks
                
                if unassigned_tasks:
                    error_detail = f"The AI model failed to assign the following tasks: {', '.join(unassigned_tasks)}. This could be due to:\n"
                    error_detail += "1. The model couldn't determine which agent best fits these tasks based on their descriptions\n"
                    error_detail += "2. The agent and task descriptions might not have clear compatibility\n\n"
                    error_detail += "Suggestions:\n"
                    error_detail += "- Try making agent descriptions more clearly aligned with tasks\n"
                    error_detail += "- Add more specific details to task descriptions\n"
                    error_detail += "- Try a different model"
                    
                    logger.error(f"Task assignment error: {error_detail}")
                    await log_llm_interaction(
                        db=db,
                        endpoint='generate-connections',
                        prompt=prompt_for_log,
                        response=content,
                        model=request.model,
                        status='error',
                        error_message=error_detail
                    )
                    raise ValueError(error_detail)
                
                # Log successful interaction
                await log_llm_interaction(
                    db=db,
                    endpoint='generate-connections',
                    prompt=prompt_for_log,
                    response=content,
                    model=request.model,
                    status='success'
                )
                
                return response_data
                
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse API response as JSON: {str(e)}"
                logger.error(error_msg)
                await log_llm_interaction(
                    db=db,
                    endpoint='generate-connections',
                    prompt=prompt_for_log,
                    response=content,
                    model=request.model,
                    status='error',
                    error_message=error_msg
                )
                raise HTTPException(status_code=500, detail=error_msg)
                
        except Exception as e:
            error_msg = f"API call failed: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback: {traceback.format_exc()}")
            await log_llm_interaction(
                db=db,
                endpoint='generate-connections',
                prompt=prompt_for_log,
                response="Error: API call failed",
                model=request.model,
                status='error',
                error_message=error_msg
            )
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        error_msg = f"Error generating connections: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/test-connections")
async def test_connections():
    """Test the connections function with sample data"""
    try:
        # Setup dummy data
        agents_info = """AVAILABLE AGENTS:

1. Agent: Test Agent
   Role: Test Role
   Goal: Test Goal
   Background: Test Background
"""

        tasks_info = """TASKS TO ASSIGN:

1. Task: Test Task
   Description: Test Description
"""

        # Get OpenAI API key
        openai_key = os.environ.get('OPENAI_API_KEY')
        if not openai_key:
            return {"error": "No OpenAI API key found in environment"}
            
        # Use OpenAI API directly
        import openai
        client = openai.OpenAI(api_key=openai_key)
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CONNECTIONS_SYSTEM_PROMPT},
                {"role": "user", "content": f"Available Agents:\n{agents_info}\n\nTasks to Assign:\n{tasks_info}"}
            ],
            temperature=0.7
        )
        
        # Extract content
        content = response.choices[0].message.content
        logger.info(f"Successfully received test API response (first 100 chars): {content[:100]}")
        
        # Parse the result
        try:
            parsed_result = json.loads(content)
            
            return {
                "success": True,
                "result": parsed_result,
                "raw_result": content[:500] + "..." if len(content) > 500 else content
            }
        except json.JSONDecodeError as json_err:
            return {
                "success": False,
                "error": f"JSON parsing error: {str(json_err)}",
                "raw_result": content[:500] + "..." if len(content) > 500 else content
            }
        
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        } 