from typing import Optional
import logging
import os
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from ..llm_config import LLMConfig, ModelProvider

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG level for more detailed logs

async def get_openai_key(db: AsyncSession) -> str:
    """Get OpenAI API key using the centralized LLMConfig.
    
    This function utilizes the LLMConfig class which handles all API key retrieval
    from various sources.
    
    Args:
        db: AsyncSession for database access to get API keys
        
    Returns:
        str: The OpenAI API key
        
    Raises:
        ValueError: If no API key can be found
    """
    # Set the provider to OPENAI
    LLMConfig.set_provider(ModelProvider.OPENAI)
    # Update the database connection
    LLMConfig.update_async_db(db)
    # Get the API key asynchronously
    api_key = await LLMConfig.get_api_key_async()
    
    if api_key == "EMPTY":
        logger.error("OpenAI API key not found in environment variables, SQLite database, or Databricks secrets")
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable, "
            "add it to the SQLite database, or configure it in Databricks secrets."
        )
    
    # Log first and last 4 characters of the key for debugging
    key_preview = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
    logger.info(f"Using OpenAI API key: {key_preview}")
    return api_key

async def get_openai_client(db: AsyncSession) -> AsyncOpenAI:
    """Get or create AsyncOpenAI client with API key from secrets using LLMConfig.
    
    This function uses the LLMConfig class to manage OpenAI client instances
    and API keys consistently throughout the application.
    
    Args:
        db: AsyncSession for database access to get API keys
        
    Returns:
        AsyncOpenAI: The OpenAI client instance
        
    Raises:
        ValueError: If no API key can be found or client cannot be created
    """
    # Configure LLMConfig for OpenAI
    LLMConfig.set_provider(ModelProvider.OPENAI)
    # Update db connection for api key retrieval
    LLMConfig.update_async_db(db)
    # Configure the client asynchronously
    await LLMConfig.configure_async()
    # Get the configured async client
    async_client = LLMConfig.get_async_client()
    
    if not async_client:
        logger.error("Failed to create AsyncOpenAI client through LLMConfig")
        raise ValueError("Failed to initialize AsyncOpenAI client")
    
    logger.debug("Successfully obtained AsyncOpenAI client from LLMConfig")
    return async_client