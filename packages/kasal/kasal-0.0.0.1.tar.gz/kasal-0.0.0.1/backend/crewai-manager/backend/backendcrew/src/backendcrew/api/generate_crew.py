from fastapi import APIRouter, HTTPException, FastAPI, Depends
from typing import Dict
from openai import AsyncOpenAI
import openai
import json
import logging
from pydantic import BaseModel
from os import getenv
import aiohttp  # For async HTTP requests
import asyncio
import litellm
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_db, LLMLog
from datetime import datetime
from ..utils.openai_utils import get_openai_client
from ..llm_config import LLMConfig, ModelProvider
from ..utils.model_config import get_model_config
import os

router = APIRouter()
logger = logging.getLogger(__name__)

class GenerationPrompt(BaseModel):
    prompt: str

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add these constants near the top of the file
DEFAULT_RECIPE_TITLE_MODEL = getenv("DEFAULT_RECIPE_TITLE_MODEL", "gpt-3.5-turbo")
DEFAULT_CREW_MODEL = getenv("DEFAULT_CREW_MODEL", "gpt-3.5-turbo")

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

app = FastAPI(title="Backendcrew API")

# Update CORS configuration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/generate-crew")
async def generate_crew(prompt: dict, db: AsyncSession = Depends(get_async_db)):
    try:
        # Log the received model and tools for debugging
        logger.info(f"Received model: {prompt.get('model', 'gpt-4-turbo')}")
        logger.info(f"Received tools: {prompt.get('tools', [])}")
        logger.info(f"Received prompt: {prompt}")
        # Use provided model or fallback to env variable, then default
        model = prompt.get("model") or getenv("CREW_MODEL", DEFAULT_CREW_MODEL)
        logger.info(f"Using model: {model}")
        model_config = get_model_config(model)
        logger.info(f"Using model config: {model_config}")
        
        # Get OpenAI client with API key from secrets
        client = await get_openai_client(db)
        
        # Build tools context for the prompt
        tools_context = ""
        if 'tools' in prompt and prompt['tools']:
            tools_context = "\n\nAvailable tools for the crew:\n"
            for tool in prompt['tools']:
                tools_context += f"- {tool}\n"
            tools_context += "\nEnsure that agents and tasks only use these available tools. If no tools are needed for a specific agent or task, leave the tools array empty."
        else:
            tools_context = "\n\nNo specific tools are available. Configure agents and tasks without tool dependencies."

        system_message = """You are an expert at creating AI crews. Based on the user's goal, generate a complete crew setup with appropriate agents and tasks.
        Each agent should be specialized and have a clear purpose. Each task should be assigned to a specific agent and have clear dependencies.""" + tools_context + """
        
        IMPORTANT: Return ONLY a valid JSON object without any markdown formatting or code block markers.
        Do not include ```json or ``` in your response.
        
        The response should be a JSON object with two arrays: 'agents' and 'tasks'.
        
        For agents include:
        {
            "agents": [
                {
                    "name": "descriptive name",
                    "role": "specific role title",
                    "goal": "clear objective",
                    "backstory": "relevant experience and expertise",
                    "tools": [],
                    "llm": "gpt-4o-mini",
                    "function_calling_llm": null,
                    "max_iter": 25,
                    "max_rpm": null,
                    "max_execution_time": null,
                    "verbose": false,
                    "allow_delegation": false,
                    "cache": true,
                    "system_template": null,
                    "prompt_template": null,
                    "response_template": null,
                    "allow_code_execution": false,
                    "code_execution_mode": "safe",
                    "max_retry_limit": 2,
                    "use_system_prompt": true,
                    "respect_context_window": true
                }
            ],
            "tasks": [
                {
                    "name": "descriptive name",
                    "description": "detailed description",
                    "expected_output": "specific deliverable format",
                    "agent": null,
                    "tools": [],
                    "async_execution": false,
                    "context_tasks": [],
                    "config": {},
                    "output_json": null,
                    "output_pydantic": null,
                    "output_file": null,
                    "output": null,
                    "callback": null,
                    "human_input": false,
                    "converter_cls": null
                }
            ]
        }
        
        Ensure:
        1. Each agent has a clear role and purpose
        2. Each task is well-defined with clear outputs
        3. Tasks are properly sequenced and dependencies are clear
        4. All fields have sensible default values
        5. An agent might have one or more tasks assigned to it.
        6. Return the name of the tool exactly as it is in the tools array."""

        # Create messages array based on model
        if model_config["name"] == "o1-preview":
            # For o1-preview, combine system and user messages into one user message
            combined_message = f"{system_message}\n\nUser request: {prompt['prompt']}"
            messages = [
                {"role": "user", "content": combined_message}
            ]
            logger.info("Using o1-preview format without system message")
        else:
            # For all other models, use standard format with system message
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt["prompt"]}
            ]
            logger.info("Using standard format with system message")

        logger.info(f"Sending messages to API: {json.dumps(messages, indent=2)}")

        # Set the provider in LLMConfig based on the model_config
        LLMConfig.set_provider(model_config["provider"])
        # Update db connection for api key retrieval
        LLMConfig.update_async_db(db)
        
        if model_config["provider"] == "openai":
            try:
                # Configure the client asynchronously
                await LLMConfig.configure_async()
                # Get the configured async client
                async_client = LLMConfig.get_async_client()
                
                if not async_client:
                    raise HTTPException(status_code=500, detail="Failed to initialize AsyncOpenAI client")
                
                response = await async_client.chat.completions.create(
                    model=model_config["name"],
                    messages=messages,
                    temperature=model_config["temperature"]
                )
                content = response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
                
        elif model_config["provider"] == "ollama":
            try:
                # Configure LiteLLM for Ollama
                await LLMConfig.configure_litellm_async()
                
                # Get API base from LLMConfig
                api_base = LLMConfig.get_api_base()
                
                # Ollama API endpoint
                ollama_url = api_base + "/api/generate"
                
                # Format messages for Ollama
                formatted_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                
                # Prepare the request
                data = {
                    "model": model_config["name"],
                    "prompt": formatted_prompt,
                    "stream": False
                }
                
                logger.info(f"Calling Ollama API with data: {json.dumps(data, indent=2)}")
                
                # Make the async API call
                async with aiohttp.ClientSession() as session:
                    async with session.post(ollama_url, json=data) as response:
                        response.raise_for_status()
                        result = await response.json()
                        content = result.get('response', '')
                        logger.info(f"Received Ollama response: {content[:200]}...")  # Log first 200 chars
                
            except aiohttp.ClientError as e:
                logger.error(f"Error calling Ollama API: {str(e)}")
                raise HTTPException(status_code=500, detail="Error calling Ollama API")
                
        elif model_config["provider"] == "anthropic":
            from anthropic import AsyncAnthropic
            
            # Configure LiteLLM for Anthropic
            await LLMConfig.configure_litellm_async()
            
            # Get the API key from the config
            api_key = await LLMConfig.get_api_key_async()
            if api_key == "EMPTY":
                raise HTTPException(status_code=500, detail="Anthropic API key is not set in the database or environment")
                
            anthropic_client = AsyncAnthropic(api_key=api_key)
            
            response = await anthropic_client.messages.create(
                model=model_config["name"],
                max_tokens=4096,
                temperature=model_config["temperature"],
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt["prompt"]}
                ]
            )
            content = response.content[0].text
            
        elif model_config["provider"] == "deepseek":
            try:
                # Turn on LiteLLM debug mode
                litellm._turn_on_debug()
                logger.info("Turned on LiteLLM debug mode")
                
                # Configure LiteLLM for deepseek
                await LLMConfig.configure_litellm_async()
                
                # Set up the API configuration
                api_key = await LLMConfig.get_api_key_async()
                api_base = LLMConfig.get_api_base()
                
                # Log API configuration for debugging
                logger.info(f"DeepSeek API Key: {api_key[:5]}... (truncated)")
                logger.info(f"DeepSeek API Base: {api_base}")
                
                # Set model name correctly
                model_name = model_config["name"]
                if not model_name.startswith("deepseek/"):
                    model_name = f"deepseek/{model_name}"
                
                # Save the model name for the configure_litellm method to check
                os.environ["DEEPSEEK_MODEL"] = model_name
                
                logger.info(f"Using DeepSeek model: {model_name}")
                
                # Use the more explicit form for the provider
                try:
                    response = await litellm.acompletion(
                        model=model_name,
                        messages=messages,
                        temperature=model_config["temperature"],
                        max_tokens=4096,
                        api_key=api_key,
                        api_base=api_base,
                        provider="deepseek"  # Explicitly set provider
                    )
                    content = response.choices[0].message.content
                except Exception as api_error:
                    logger.error(f"DeepSeek API call failed: {str(api_error)}")
                    
                    # Check for common authentication issues
                    error_msg = str(api_error)
                    if "Authentication Fails" in error_msg or "authentication_error" in error_msg:
                        logger.error("This is an authentication error. Please check your DeepSeek API key.")
                        logger.error("Make sure the DEEPSEEK_API_KEY environment variable is set correctly.")
                        
                        # Try to check the environment variable directly
                        env_key = os.getenv("DEEPSEEK_API_KEY", "Not set")
                        if env_key == "Not set":
                            logger.error("DEEPSEEK_API_KEY environment variable is not set!")
                        else:
                            logger.error(f"DEEPSEEK_API_KEY environment variable is set (length: {len(env_key)})")
                    
                    # Re-raise for the outer exception handler
                    raise
            except Exception as e:
                logger.error(f"Error calling Deepseek API: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error calling Deepseek API: {str(e)}")
                
        elif model_config["provider"] == "databricks":
            try:
                # Configure LiteLLM for Databricks
                await LLMConfig.configure_litellm_async()
                
                # Set up the API configuration
                api_key = await LLMConfig.get_api_key_async()
                api_base = LLMConfig.get_api_base()
                
                # Set model name correctly
                model_name = model_config["name"]
                if not model_name.startswith("databricks/"):
                    model_name = f"databricks/{model_name}"
                
                logger.info(f"Using Databricks model: {model_name}")
                
                response = await litellm.acompletion(
                    model=model_name,
                    messages=messages,
                    temperature=model_config["temperature"],
                    max_tokens=4096,
                    api_key=api_key,
                    api_base=api_base
                )
                content = response.choices[0].message.content
            except Exception as e:
                logger.error(f"Error calling Databricks API: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error calling Databricks API: {str(e)}")

        logger.info(f"Generated crew setup: {content}")

        try:
            setup = json.loads(content)
            
            # Validate structure
            if not isinstance(setup.get('agents'), list) or not isinstance(setup.get('tasks'), list):
                raise ValueError("Invalid response structure")

            # Add IDs to agents if they don't exist
            for i, agent in enumerate(setup['agents']):
                if 'id' not in agent:
                    agent['id'] = str(i)  # Convert to string for consistency
                
                # Ensure tools is a list
                if not isinstance(agent.get('tools'), list):
                    agent['tools'] = []

                # Ensure default values for agent configuration
                agent.setdefault("llm", "gpt-4o-mini")
                agent.setdefault("function_calling_llm", None)
                agent.setdefault("max_iter", 25)
                agent.setdefault("max_rpm", None)
                agent.setdefault("max_execution_time", None)
                agent.setdefault("verbose", False)
                agent.setdefault("allow_delegation", False)
                agent.setdefault("cache", True)
                agent.setdefault("system_template", None)
                agent.setdefault("prompt_template", None)
                agent.setdefault("response_template", None)
                agent.setdefault("allow_code_execution", False)
                agent.setdefault("code_execution_mode", "safe")
                agent.setdefault("max_retry_limit", 2)
                agent.setdefault("use_system_prompt", True)
                agent.setdefault("respect_context_window", True)

            # Add IDs to tasks and convert agent_id to assigned_agent if needed
            for i, task in enumerate(setup['tasks']):
                if 'id' not in task:
                    task['id'] = str(i)

                # Convert agent_id to assigned_agent if needed
                if 'agent_id' in task and 'assigned_agent' not in task:
                    # Get the corresponding agent's role
                    if isinstance(task['agent_id'], int) and task['agent_id'] < len(setup['agents']):
                        agent = setup['agents'][task['agent_id']]
                        task['assigned_agent'] = agent['role'].lower().replace(' ', '_')
                    del task['agent_id']
                
                # Ensure tools is a list
                if not isinstance(task.get('tools'), list):
                    task['tools'] = []

                # Ensure default values for task configuration
                task.setdefault("async_execution", False)
                task.setdefault("context_tasks", [])
                task.setdefault("config", {})
                task.setdefault("output_json", None)
                task.setdefault("output_pydantic", None)
                task.setdefault("output_file", None)
                task.setdefault("output", None)
                task.setdefault("callback", None)
                task.setdefault("human_input", False)
                task.setdefault("converter_cls", None)

            logger.info(f"Processed setup: {json.dumps(setup, indent=2)}")
            # Log the successful interaction
            await log_llm_interaction(
                db=db,
                endpoint='generate-crew',
                prompt=f"System: {system_message}\nUser: {prompt['prompt']}",
                response=content,
                model=model_config["name"]
            )

            return setup
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response")
        except ValueError as e:
            logger.error(f"Invalid crew setup: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Error generating crew: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-recipe-title")
async def generate_recipe_title(prompt: GenerationPrompt, db: AsyncSession = Depends(get_async_db)):
    try:
        model = getenv("RECIPE_TITLE_MODEL", DEFAULT_RECIPE_TITLE_MODEL)
        system_message = """You are an expert at creating concise, descriptive titles. 
        Given a description of an AI crew's purpose, create a clear and professional title that captures the essence of what the crew does.
        The title should be 3-6 words long and use professional terminology.
        Do not use quotes or special characters. Just return the title directly."""

        # Get OpenAI client with API key from secrets using LLMConfig
        LLMConfig.set_provider(ModelProvider.OPENAI)
        # Update db connection for api key retrieval
        LLMConfig.update_async_db(db)
        # Configure the client asynchronously
        await LLMConfig.configure_async()
        # Get the configured async client
        async_client = LLMConfig.get_async_client()
        
        if not async_client:
            raise HTTPException(status_code=500, detail="Failed to initialize AsyncOpenAI client")

        response = await async_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt.prompt}
            ],
            temperature=0.7,
            max_tokens=30
        )

        title = response.choices[0].message.content.strip()
        logger.info(f"Generated recipe title: {title}")

        # Log the successful interaction
        await log_llm_interaction(
            db=db,
            endpoint='generate-recipe-title',
            prompt=f"System: {system_message}\nUser: {prompt.prompt}",
            response=title,
            model=model
        )

        return {"title": title}

    except Exception as e:
        # Log the failed interaction
        await log_llm_interaction(
            db=db,
            endpoint='generate-recipe-title',
            prompt=prompt.prompt,
            response="",
            model=model,
            status='error',
            error_message=str(e)
        )
        logger.error(f"Error generating recipe title: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

