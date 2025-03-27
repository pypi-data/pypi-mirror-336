from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import json
import logging
from ..database import get_async_db
from ..utils.openai_utils import get_openai_client
from datetime import datetime
from ..database import LLMLog
from os import getenv
from ..utils.model_config import get_model_config

router = APIRouter()
logger = logging.getLogger(__name__)

class TemplateRequest(BaseModel):
    role: str
    goal: str
    backstory: str
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

@router.post("/generate-templates")
async def generate_templates(request: TemplateRequest, db: AsyncSession = Depends(get_async_db)):
    try:
        model_config = get_model_config(request.model)
        
        system_message = """You are an expert at creating AI agent templates following CrewAI and LangChain best practices.
        Given an agent's role, goal, and backstory, generate three templates:
        1. System Template: Defines the agent's core identity and capabilities
        2. Prompt Template: Structures how tasks are presented to the agent
        3. Response Template: Guides how the agent should format its responses

        Follow these principles:
        - System Template should establish expertise, boundaries, and ethical guidelines
        - Prompt Template should include placeholders for task-specific information
        - Response Template should enforce structured, actionable outputs
        - Use {variables} for dynamic content
        - Keep templates concise but comprehensive
        - Ensure templates work together cohesively

        IMPORTANT: Return a JSON object with exactly these field names:
        {
            "system_template": "your system template here",
            "prompt_template": "your prompt template here",
            "response_template": "your response template here"
        }"""

        # Get OpenAI client with API key from secrets
        client = await get_openai_client(db)

        # Create the user prompt with agent details
        user_prompt = f"""Create templates for an AI agent with:
        Role: {request.role}
        Goal: {request.goal}
        Backstory: {request.backstory}

        Generate all three templates following CrewAI and LangChain best practices."""

        response = await client.chat.completions.create(
            model=model_config["name"],
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        logger.info(f"Generated templates: {content}")

        try:
            templates = json.loads(content)
            
            # Normalize the field names to lowercase if needed
            normalized_templates = {
                "system_template": templates.get("system_template") or templates.get("System Template") or templates.get("System_Template"),
                "prompt_template": templates.get("prompt_template") or templates.get("Prompt Template") or templates.get("Prompt_Template"),
                "response_template": templates.get("response_template") or templates.get("Response Template") or templates.get("Response_Template")
            }
            
            # Validate that all required fields are present and non-empty
            for field, value in normalized_templates.items():
                if not value:
                    raise ValueError(f"Missing or empty required field: {field}")

            # Log the successful interaction
            await log_llm_interaction(
                db=db,
                endpoint='generate-templates',
                prompt=f"System: {system_message}\nUser: {user_prompt}",
                response=content,
                model=model_config["name"]
            )

            return normalized_templates

        except json.JSONDecodeError:
            logger.error(f"Failed to parse AI response as JSON: {content}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response")
        except ValueError as e:
            logger.error(f"Invalid templates: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        logger.error(f"Error generating templates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 