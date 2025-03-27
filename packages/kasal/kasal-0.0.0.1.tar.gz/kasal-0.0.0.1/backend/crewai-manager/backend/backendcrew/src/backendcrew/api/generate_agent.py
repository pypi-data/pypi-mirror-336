from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import json
import logging
from os import getenv
from datetime import datetime
from ..database import get_async_db, LLMLog
from ..llm_config import LLMConfig, ModelProvider
from ..utils.model_config import get_model_config

router = APIRouter()
logger = logging.getLogger(__name__)

class AgentPrompt(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

async def log_llm_interaction(db, endpoint, prompt, response, model):
    """Log LLM interaction to the database"""
    try:
        log_entry = LLMLog(
            endpoint=endpoint,
            prompt=prompt,
            response=response,
            model=model,
            status='success',
            created_at=datetime.utcnow()
        )
        db.add(log_entry)
        await db.commit()
        logger.info(f"Logged {endpoint} interaction to database")
    except Exception as e:
        logger.error(f"Failed to log LLM interaction: {str(e)}")
        await db.rollback()


@router.post("/generate-agent")
async def generate_agent(prompt: dict, db: AsyncSession = Depends(get_async_db)):
    try:
        # Use LLMConfig for database and API configuration
        LLMConfig.update_async_db(db)
        
        # Log the raw request payload for debugging
        logger.info(f"Received generate-agent request: {json.dumps(prompt)}")
        
        # Get model from request payload or fallback to environment variable or default
        model = prompt.get("model") or getenv("AGENT_MODEL", "gpt-4o-mini")
        logger.info(f"Using model for agent generation: {model}")
        
        # Get model configuration based on model name
        model_config = get_model_config(model)
        provider = model_config["provider"]
        logger.info(f"Using provider: {provider} for model: {model}")
        logger.info(f"Full model config: {json.dumps(model_config)}")
        
        # Configure environment for the specific provider
        LLMConfig.set_provider(provider)
        
        # Apply provider-specific configuration
        if provider == ModelProvider.OPENAI:
            LLMConfig.setup_openai_for_agent()
        elif provider == ModelProvider.ANTHROPIC:
            LLMConfig.setup_anthropic_for_agent()
        elif provider == ModelProvider.DEEPSEEK:
            LLMConfig.setup_deepseek_for_agent()
        elif provider == ModelProvider.OLLAMA:
            LLMConfig.setup_ollama_for_agent()
        elif provider == ModelProvider.DATABRICKS:
            LLMConfig.setup_databricks_for_agent()
        
        system_message = """You are an expert at creating AI agents. Based on the user's description, generate a complete agent setup.
        Format your response as a JSON object with the following structure:
        {
            "name": "descriptive name",
            "role": "specific role title",
            "goal": "clear objective",
            "backstory": "relevant experience and expertise",
            "tools": [],
            "advanced_config": {
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
        }
        
        Make sure to:
        1. Give the agent a descriptive name
        2. Define a clear and specific role
        3. Set a concrete goal aligned with the role
        4. Write a detailed backstory that explains their expertise
        5. Keep the advanced configuration with default values unless specifically needed
        6. Tools should be an empty array"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt["prompt"]}
        ]

        # Use LLMConfig.generate_async_completion with the configured environment
        logger.info(f"Generating agent with model: {model}")
        response = await LLMConfig.generate_async_completion(
            model=model,
            messages=messages,
            temperature=0.7,
            db=db
        )

        # Extract content from the response
        content = response["choices"][0]["message"]["content"]
        logger.info(f"Generated agent setup: {content}")

        try:
            setup = json.loads(content)
            
            # Validate required fields
            required_fields = ["name", "role", "goal", "backstory"]
            for field in required_fields:
                if field not in setup:
                    raise ValueError(f"Missing required field: {field}")
            
            # Update the advanced_config.llm field to use the selected model
            if "advanced_config" not in setup:
                setup["advanced_config"] = {
                    "llm": model,  # Use the specified model
                    "function_calling_llm": None,
                    "max_iter": 25,
                    "max_rpm": None,
                    "max_execution_time": None,
                    "verbose": False,
                    "allow_delegation": False,
                    "cache": True,
                    "system_template": None,
                    "prompt_template": None,
                    "response_template": None,
                    "allow_code_execution": False,
                    "code_execution_mode": "safe",
                    "max_retry_limit": 2,
                    "use_system_prompt": True,
                    "respect_context_window": True
                }
            else:
                # Update the LLM field in advanced_config to use the selected model
                setup["advanced_config"]["llm"] = model
            
            # Ensure tools exists
            if "tools" not in setup:
                setup["tools"] = []

            # Log the successful interaction
            await log_llm_interaction(
                db=db,
                endpoint='generate-agent',
                prompt=f"System: {system_message}\nUser: {prompt['prompt']}",
                response=content,
                model=model
            )

            return setup
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response")
        except ValueError as e:
            logger.error(f"Invalid agent setup: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        logger.error(f"Error generating agent: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 