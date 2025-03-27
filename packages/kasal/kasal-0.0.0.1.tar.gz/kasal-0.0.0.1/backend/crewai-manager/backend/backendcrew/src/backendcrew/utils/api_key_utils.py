import os
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
import litellm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import ApiKey
from ..api.keys import decrypt_value
from .logger_manager import LoggerManager
from ..llm_config import LLMConfig, ModelProvider

# Initialize logger
logger_manager = LoggerManager()

def setup_provider_api_key(db: Session, key_name: str) -> bool:
    """
    Generic function to set up an API key from the database.
    
    Args:
        db (Session): Database session
        key_name (str): Name of the API key to set up (e.g., "OPENAI_API_KEY", "DEEPSEEK_API_KEY")
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Query the database directly
        result = db.execute(select(ApiKey).where(ApiKey.name == key_name))
        api_key_record = result.scalars().first()
        
        if not api_key_record:
            logger_manager.crew.warning(f"No {key_name} found in database")
            return False
            
        # Decrypt the value
        api_key = decrypt_value(api_key_record.encrypted_value)
        
        if not api_key:
            logger_manager.crew.error(f"Failed to decrypt {key_name} from database")
            return False
            
        # Set the environment variable only, avoid setting litellm globals
        os.environ[key_name] = api_key
        
        # Basic environment variable setup for each provider
        # We avoid touching litellm globals here to prevent conflicts
        if key_name == "OPENAI_API_KEY":
            # Only set environment variable
            os.environ["OPENAI_API_KEY"] = api_key
            # Save previous key for backup
            os.environ["PREVIOUS_OPENAI_API_KEY"] = api_key
            
        elif key_name == "DEEPSEEK_API_KEY":
            # Set DeepSeek-specific environment variables only
            deepseek_base_url = os.environ.get("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/v1")
            os.environ["DEEPSEEK_ENDPOINT"] = deepseek_base_url
            os.environ["DEEPSEEK_API_KEY"] = api_key
            
            # Log configuration for debugging
            logger_manager.crew.info(f"DeepSeek API Base URL: {deepseek_base_url}")
            logger_manager.crew.info(f"DeepSeek API Key (first 4 chars): {api_key[:4]}...")
            
        elif key_name == "ANTHROPIC_API_KEY":
            # Set Anthropic-specific environment variables
            os.environ["ANTHROPIC_API_KEY"] = api_key
            
            # Log configuration for debugging
            logger_manager.crew.info(f"Anthropic API Key (first 8 chars): {api_key[:8]}...")
            
            # Validate key format
            if not api_key.startswith("sk-ant-"):
                logger_manager.crew.warning(f"Anthropic API key doesn't start with 'sk-ant-' - this might cause issues")
            
        logger_manager.crew.info(f"Successfully set {key_name} from database")
        
        # Verify the environment variable was set
        env_key = os.getenv(key_name)
        if env_key and env_key == api_key:
            logger_manager.crew.info(f"Verified {key_name} environment variable is set correctly")
            return True
        else:
            logger_manager.crew.warning(f"{key_name} environment variable verification failed")
            return False
            
    except Exception as e:
        logger_manager.crew.error(f"Error setting {key_name} from database: {str(e)}")
        return False

async def async_setup_provider_api_key(db: AsyncSession, key_name: str) -> bool:
    """
    Async version of setup_provider_api_key for use with AsyncSession.
    
    Args:
        db (AsyncSession): Async database session
        key_name (str): Name of the API key to set up (e.g., "OPENAI_API_KEY", "DEEPSEEK_API_KEY")
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Query the database using async methods
        query = select(ApiKey).where(ApiKey.name == key_name)
        result = await db.execute(query)
        api_key_record = result.scalars().first()
        
        if not api_key_record:
            logger_manager.crew.warning(f"No {key_name} found in database")
            return False
            
        # Decrypt the value
        api_key = decrypt_value(api_key_record.encrypted_value)
        
        if not api_key:
            logger_manager.crew.error(f"Failed to decrypt {key_name} from database")
            return False
        
        # Set the environment variable only, avoid setting litellm globals
        os.environ[key_name] = api_key
        
        # Basic environment variable setup for each provider
        # We avoid touching litellm globals here to prevent conflicts
        if key_name == "OPENAI_API_KEY":
            # Only set environment variable
            os.environ["OPENAI_API_KEY"] = api_key
            # Save previous key for backup
            os.environ["PREVIOUS_OPENAI_API_KEY"] = api_key
            
        elif key_name == "DEEPSEEK_API_KEY":
            # Set DeepSeek-specific environment variables only
            deepseek_base_url = os.environ.get("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/v1")
            os.environ["DEEPSEEK_ENDPOINT"] = deepseek_base_url
            os.environ["DEEPSEEK_API_KEY"] = api_key
            
            # Log configuration for debugging
            logger_manager.crew.info(f"DeepSeek API Base URL: {deepseek_base_url}")
            logger_manager.crew.info(f"DeepSeek API Key (first 4 chars): {api_key[:4]}...")
            
        elif key_name == "ANTHROPIC_API_KEY":
            # Set Anthropic-specific environment variables
            os.environ["ANTHROPIC_API_KEY"] = api_key
            
            # Log configuration for debugging
            logger_manager.crew.info(f"Anthropic API Key (first 8 chars): {api_key[:8]}...")
            
            # Validate key format
            if not api_key.startswith("sk-ant-"):
                logger_manager.crew.warning(f"Anthropic API key doesn't start with 'sk-ant-' - this might cause issues")
            
        logger_manager.crew.info(f"Successfully set {key_name} from database")
        
        # Verify the environment variable was set
        env_key = os.getenv(key_name)
        if env_key and env_key == api_key:
            logger_manager.crew.info(f"Verified {key_name} environment variable is set correctly")
            return True
        else:
            logger_manager.crew.warning(f"{key_name} environment variable verification failed")
            return False
            
    except Exception as e:
        logger_manager.crew.error(f"Error setting {key_name} from database: {str(e)}")
        return False

async def async_setup_openai_api_key(db: AsyncSession) -> bool:
    """Set up the OpenAI API key from the database using async."""
    return await async_setup_provider_api_key(db, "OPENAI_API_KEY")

async def async_setup_deepseek_api_key(db: AsyncSession) -> bool:
    """Set up the DeepSeek API key from the database using async."""
    return await async_setup_provider_api_key(db, "DEEPSEEK_API_KEY")

async def async_setup_anthropic_api_key(db: AsyncSession) -> bool:
    """Set up the Anthropic API key from the database using async."""
    return await async_setup_provider_api_key(db, "ANTHROPIC_API_KEY")

async def async_setup_all_api_keys(db: AsyncSession) -> None:
    """Set up all supported API keys from the database using async."""
    # Import LLMConfig to check current provider
    current_provider = LLMConfig.get_provider() if hasattr(LLMConfig, 'get_provider') else "unknown"
    logger_manager.crew.info(f"[API_KEYS] Current provider before setup: {current_provider}")
    
    # Always set up OpenAI API key (commonly needed)
    openai_success = await async_setup_openai_api_key(db)
    logger_manager.crew.info(f"OpenAI API key setup: {'Successful' if openai_success else 'Failed'}")
    
    # Only set up DeepSeek API key if provider is DeepSeek
    if current_provider == ModelProvider.DEEPSEEK:
        logger_manager.crew.info("[API_KEYS] Provider is DeepSeek, setting up DeepSeek API key")
        deepseek_success = await async_setup_deepseek_api_key(db)
        logger_manager.crew.info(f"DeepSeek API key setup: {'Successful' if deepseek_success else 'Failed'}")
    else:
        logger_manager.crew.info(f"[API_KEYS] Provider is {current_provider}, skipping DeepSeek API key setup")
        
    # Set up Anthropic API key if provider is Anthropic
    if current_provider == ModelProvider.ANTHROPIC:
        logger_manager.crew.info("[API_KEYS] Provider is Anthropic, setting up Anthropic API key")
        anthropic_success = await async_setup_anthropic_api_key(db)
        logger_manager.crew.info(f"Anthropic API key setup: {'Successful' if anthropic_success else 'Failed'}")
    else:
        logger_manager.crew.info(f"[API_KEYS] Provider is {current_provider}, skipping Anthropic API key setup")
    
    # Check if litellm provider settings need to be reset
    # Let LLMConfig handle this by initializing it
    logger_manager.crew.info("[API_KEYS] Ensuring LiteLLM configuration is consistent")
    LLMConfig.initialize()

def setup_openai_api_key(db: Session) -> bool:
    """Set up the OpenAI API key from the database."""
    return setup_provider_api_key(db, "OPENAI_API_KEY")

def setup_deepseek_api_key(db: Session) -> bool:
    """Set up the DeepSeek API key from the database."""
    return setup_provider_api_key(db, "DEEPSEEK_API_KEY")

def setup_anthropic_api_key(db: Session) -> bool:
    """Set up the Anthropic API key from the database."""
    return setup_provider_api_key(db, "ANTHROPIC_API_KEY")

def setup_all_api_keys(db: Session) -> None:
    """Set up all supported API keys from the database."""
    # Import LLMConfig to check current provider
    current_provider = LLMConfig.get_provider() if hasattr(LLMConfig, 'get_provider') else "unknown"
    logger_manager.crew.info(f"[API_KEYS] Current provider before setup: {current_provider}")
    
    # Always set up OpenAI API key (commonly needed)
    openai_success = setup_openai_api_key(db)
    logger_manager.crew.info(f"OpenAI API key setup: {'Successful' if openai_success else 'Failed'}")
    
    # Set up DeepSeek API key if provider is DeepSeek
    if current_provider == ModelProvider.DEEPSEEK:
        logger_manager.crew.info("[API_KEYS] Provider is DeepSeek, setting up DeepSeek API key")
        deepseek_success = setup_deepseek_api_key(db)
        logger_manager.crew.info(f"DeepSeek API key setup: {'Successful' if deepseek_success else 'Failed'}")
    else:
        logger_manager.crew.info(f"[API_KEYS] Provider is {current_provider}, skipping DeepSeek API key setup")
    
    # Set up Anthropic API key if provider is Anthropic
    if current_provider == ModelProvider.ANTHROPIC:
        logger_manager.crew.info("[API_KEYS] Provider is Anthropic, setting up Anthropic API key")
        anthropic_success = setup_anthropic_api_key(db)
        logger_manager.crew.info(f"Anthropic API key setup: {'Successful' if anthropic_success else 'Failed'}")
    else:
        logger_manager.crew.info(f"[API_KEYS] Provider is {current_provider}, skipping Anthropic API key setup")
    
    # Check if litellm provider settings need to be reset
    # Let LLMConfig handle this by initializing it
    logger_manager.crew.info("[API_KEYS] Ensuring LiteLLM configuration is consistent") 
    LLMConfig.initialize() 