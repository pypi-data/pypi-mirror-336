from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import json
import logging
from ..database import get_async_db
from datetime import datetime
from ..database import LLMLog
from os import getenv
from ..llm_config import LLMConfig

router = APIRouter()
logger = logging.getLogger(__name__)

# Add these constants near the top of the file
DEFAULT_TASK_MODEL = getenv("DEFAULT_TASK_MODEL", "gpt-4o-mini")

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

@router.post("/generate-task")
async def generate_task(prompt: dict, db: AsyncSession = Depends(get_async_db)):
    try:
        # Update the async db in LLMConfig
        LLMConfig.update_async_db(db)
        
        # Get model from request payload or fallback to environment variables
        model = prompt.get("model") or getenv("TASK_MODEL", DEFAULT_TASK_MODEL)
        logger.info(f"Using model for task generation: {model}")
        
        # Create the system message with proper JSON formatting instructions
        base_message = """You are an expert at creating AI tasks. Generate a complete task configuration with all settings.
        Format your response as a JSON object with the following structure:
        {
            "name": "descriptive name",
            "description": "detailed description of what needs to be done",
            "expected_output": "clear description of the expected deliverable",
            "advanced_config": {
                "async_execution": false,
                "context_tasks": [],
                "output_json": null,
                "output_pydantic": null,
                "output_file": null,
                "human_input": false,
                "retry_on_fail": true,
                "max_retries": 3,
                "timeout": null,
                "priority": 1,
                "dependencies": [],
                "callback": null,
                "error_handling": "default",
                "output_parser": null,
                "cache_response": true,
                "cache_ttl": 3600
            }
        }
        
        Make sure to:
        1. Give the task a clear, descriptive name
        2. Write a detailed description that explains exactly what needs to be done
        3. Specify the expected output format and requirements
        4. Keep advanced configuration with sensible defaults
        5. Tools should be an empty array"""
        
        # Add agent context if provided
        if 'agent' in prompt and prompt['agent']:
            agent = prompt['agent']
            base_message += f"\n\nCreate a task specifically for an agent with the following profile:\n"
            base_message += f"Name: {agent['name']}\n"
            base_message += f"Role: {agent['role']}\n"
            base_message += f"Goal: {agent['goal']}\n"
            base_message += f"Backstory: {agent['backstory']}\n"
            base_message += "\nEnsure the task aligns with this agent's expertise and goals."

        # Make the API call using LLMConfig
        messages = [
            {"role": "system", "content": base_message},
            {"role": "user", "content": prompt["text"]}
        ]
        response = await LLMConfig.generate_async_completion(
            model=model,
            messages=messages,
            temperature=0.7,
            db=db
        )
        
        content = response.choices[0].message.content
        # Clean the content by removing markdown formatting
        content = content.replace('```json', '').replace('```', '').strip()
        logger.info(f"Generated task setup: {content}")

        try:
            setup = json.loads(content)
            
            # Validate required fields
            required_fields = ['name', 'description', 'expected_output']
            for field in required_fields:
                if field not in setup:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set empty tools array
            setup["tools"] = []

            # Ensure advanced_config exists with defaults if not provided
            if "advanced_config" not in setup:
                setup["advanced_config"] = {
                    "async_execution": False,
                    "context_tasks": [],
                    "output_json": None,
                    "output_pydantic": None,
                    "output_file": None,
                    "human_input": False,
                    "retry_on_fail": True,
                    "max_retries": 3,
                    "timeout": None,
                    "priority": 1,
                    "dependencies": [],
                    "callback": None,
                    "error_handling": "default",
                    "output_parser": None,
                    "cache_response": True,
                    "cache_ttl": 3600
                }

            # Log the successful interaction
            await log_llm_interaction(
                db=db,
                endpoint='generate-task',
                prompt=f"System: {base_message}\nUser: {prompt['text']}",
                response=content,
                model=model
            )

            return setup
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response")
        except ValueError as e:
            logger.error(f"Invalid task setup: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Error generating task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 