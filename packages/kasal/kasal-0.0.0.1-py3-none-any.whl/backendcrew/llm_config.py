import os
import logging
from enum import Enum
import openai
import litellm
from openai import OpenAI, AsyncOpenAI
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
import functools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    DEEPSEEK = "deepseek"
    DATABRICKS = "databricks"

# List of supported models per provider
SUPPORTED_MODELS = {
    ModelProvider.OPENAI: [
        "gpt-4-turbo-preview",
        "gpt-4",
        "gpt-4-0125-preview",
        "gpt-4-1106-preview",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-1106",
        "gpt-4o-mini",
        "gpt-4o",
        "o1-mini",
        "o1",
        "o3-mini",
        "o3-mini-high"
    ],
    ModelProvider.OLLAMA: [
        "qwen2.5:32b",
        "llama2",
        "llama2:13b",
        "llama3.2:latest",
        "mistral",
        "mixtral",
        "codellama",
        "mistral-nemo:12b-instruct-2407-q2_K",
        "llama3.2:3b-text-q8_0"
    ],
    ModelProvider.ANTHROPIC: [
        "claude-3-opus-20240229",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-7-sonnet-20250219",
        "claude-3-7-sonnet-20250219-thinking",
        "claude-3-sonnet",
        "claude-2.1",
        "claude-2.0",
    ],
    ModelProvider.DATABRICKS: [
        "databricks-meta-llama-3-3-70b-instruct",
        "databricks-meta-llama-3-1-405b-instruct",
    ],
    ModelProvider.DEEPSEEK: [
        "deepseek-chat",
        "deepseek-reasoner",
    ]
}

class LLMConfig:
    """
    Centralized configuration for LLM providers and models.
    Handles API keys, base URLs, and dynamic provider switching.
    """
    _client: Optional[OpenAI] = None
    _async_client: Optional[AsyncOpenAI] = None
    _provider: str = ModelProvider.OPENAI
    _api_base: Optional[str] = None
    _api_key: Optional[str] = None
    _db: Optional[Session] = None
    _async_db: Optional[AsyncSession] = None

    @classmethod
    def set_provider(cls, provider: str) -> None:
        """Set the LLM provider."""
        cls._provider = provider.lower()
        cls._client = None  # Reset client when provider changes

    @classmethod
    def get_provider(cls) -> str:
        """Get the configured LLM provider."""
        return cls._provider

    @classmethod
    def set_api_base(cls, api_base: str) -> None:
        """Set the API base URL."""
        cls._api_base = api_base
        cls._client = None  # Reset client when API base changes

    @classmethod
    def get_api_base(cls) -> str:
        """Get the API base URL for the current provider."""
        if cls._api_base:
            return cls._api_base
            
        # Use provider-specific defaults
        if cls._provider == ModelProvider.OLLAMA:
            return "http://localhost:11434"
        elif cls._provider == ModelProvider.DATABRICKS:
            return os.getenv("DATABRICKS_ENDPOINT", "https://e2-demo-west.cloud.databricks.com/serving-endpoints")
        elif cls._provider == ModelProvider.DEEPSEEK:
            return os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com")
        else:
            return ""  # Default OpenAI URL will be used

    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """Set the API key."""
        cls._api_key = api_key
        cls._client = None  # Reset client when API key changes
    
    @classmethod
    def update_db(cls, db: Session) -> None:
        """Update the database session used for API key retrieval."""
        cls._db = db
        cls._client = None  # Reset client to force re-fetching of API keys
        
    @classmethod
    def update_async_db(cls, db: AsyncSession) -> None:
        """Update the async database session used for API key retrieval."""
        cls._async_db = db
        cls._client = None  # Reset client to force re-fetching of API keys

    @classmethod
    def get_api_key(cls) -> str:
        """Get the API key for the current provider (synchronous)."""
        # If a key was set manually, use it
        if cls._api_key:
            return cls._api_key
        
        # If we have a database connection, try to get the key from there
        if cls._db:
            from .utils.api_key_utils import setup_provider_api_key
            
            # Determine which key to fetch based on provider
            key_name = None
            if cls._provider == ModelProvider.OLLAMA:
                return "EMPTY"
            elif cls._provider == ModelProvider.DATABRICKS:
                key_name = "DATABRICKS_TOKEN"
            elif cls._provider == ModelProvider.DEEPSEEK:
                key_name = "DEEPSEEK_API_KEY" 
            elif cls._provider == ModelProvider.ANTHROPIC:
                key_name = "ANTHROPIC_API_KEY"
            else:  # Default to OpenAI
                key_name = "OPENAI_API_KEY"
            
            # If we have a key name, try to get it from the database
            if key_name:
                success = setup_provider_api_key(cls._db, key_name)
                if success:
                    return os.getenv(key_name, "EMPTY")
        
        # Fall back to environment variables if database retrieval fails or no DB connection
        if cls._provider == ModelProvider.OLLAMA:
            return "EMPTY"  # Ollama doesn't require an API key
        elif cls._provider == ModelProvider.DATABRICKS:
            return os.getenv("DATABRICKS_TOKEN", "EMPTY")
        elif cls._provider == ModelProvider.DEEPSEEK:
            return os.getenv("DEEPSEEK_API_KEY", "EMPTY")
        elif cls._provider == ModelProvider.ANTHROPIC:
            key = os.getenv("ANTHROPIC_API_KEY", "EMPTY")
            if key == "EMPTY" or not key.startswith("sk-ant-"):
                logger.warning("Anthropic API key doesn't start with 'sk-ant-' - this is unusual but may work with newer key formats")
            return key
        else:
            return os.getenv("OPENAI_API_KEY", "EMPTY")

    @classmethod
    async def get_api_key_async(cls) -> str:
        """Get the API key for the current provider (async version)."""
        # If a key was set manually, use it
        if cls._api_key:
            return cls._api_key
        
        # If we have an async database connection, try to get the key from there
        if cls._async_db:
            from .utils.api_key_utils import async_setup_provider_api_key
            
            # Determine which key to fetch based on provider
            key_name = None
            if cls._provider == ModelProvider.OLLAMA:
                return "EMPTY"
            elif cls._provider == ModelProvider.DATABRICKS:
                key_name = "DATABRICKS_TOKEN"
            elif cls._provider == ModelProvider.DEEPSEEK:
                key_name = "DEEPSEEK_API_KEY" 
            elif cls._provider == ModelProvider.ANTHROPIC:
                key_name = "ANTHROPIC_API_KEY"
            else:  # Default to OpenAI
                key_name = "OPENAI_API_KEY"
            
            # If we have a key name, try to get it from the database
            if key_name:
                success = await async_setup_provider_api_key(cls._async_db, key_name)
                if success:
                    return os.getenv(key_name, "EMPTY")
        
        # Fall back to environment variables
        return cls.get_api_key()  # Reuse the synchronous method for consistency

    @classmethod
    async def configure_async(cls) -> None:
        """Configure the LLM environment for async operations."""
        if cls._provider != ModelProvider.OLLAMA:
            api_key = await cls.get_api_key_async()
            api_base = cls.get_api_base()
            
            # Set OpenAI global variables
            openai.api_key = api_key
            if api_base:
                openai.api_base = api_base
            
            # Set up an AsyncOpenAI client
            cls._async_client = AsyncOpenAI(
                api_key=api_key,
                base_url=api_base if api_base else None
            )
            logger.info(f"Configured AsyncOpenAI client for {cls._provider}")

    @classmethod
    def get_client(cls) -> OpenAI:
        """Get the configured OpenAI client instance."""
        if cls._client is None:
            cls.configure()
        return cls._client

    @classmethod
    def get_async_client(cls) -> AsyncOpenAI:
        """Get the configured AsyncOpenAI client instance."""
        if cls._async_client is None:
            logger.warning("AsyncOpenAI client requested but not configured. Returning None.")
            return None
        return cls._async_client

    @classmethod
    def get_default_model(cls, provider: str = None) -> str:
        """Get the default model for a provider."""
        if not provider:
            provider = cls._provider
            
        if provider == ModelProvider.OLLAMA:
            return "qwen2.5:32b"
        elif provider == ModelProvider.ANTHROPIC:
            return "claude-3-opus"
        elif provider == ModelProvider.DATABRICKS:
            return "databricks-meta-llama-3-3-70b-instruct"
        elif provider == ModelProvider.DEEPSEEK:
            return "deepseek-chat"
        else:
            return "gpt-4o-mini"  # Default OpenAI model

    @staticmethod
    def validate_model(model: str) -> bool:
        """Validate if the specified model is supported."""
        if not model:
            return True  # Default model will be used
            
        # Check if model is in any of the supported providers
        for provider, models in SUPPORTED_MODELS.items():
            if model in models:
                return True
                
        return False

    @classmethod
    def _detect_provider_from_model(cls, model: str) -> str:
        """Detect the model provider based on the model name."""
        if not model:
            return None
            
        model_lower = model.lower()
        
        # Check for provider prefixes (e.g., "openai/gpt-4")
        if "/" in model_lower:
            parts = model_lower.split("/")
            if len(parts) > 1:
                prefix = parts[0]
                if prefix in ["openai", "anthropic", "deepseek", "databricks", "ollama"]:
                    return f"ModelProvider.{prefix.upper()}"
                model_lower = parts[1]  # Use the model part for further detection
        
        # Check by model name patterns
        if model_lower.startswith(("gpt-", "text-")) or model_lower.startswith(("o1", "o3")) or model_lower in SUPPORTED_MODELS[ModelProvider.OPENAI]:
            return ModelProvider.OPENAI
        elif model_lower.startswith("claude-") or model_lower in SUPPORTED_MODELS[ModelProvider.ANTHROPIC]:
            return ModelProvider.ANTHROPIC
        elif "deepseek" in model_lower or model_lower in SUPPORTED_MODELS[ModelProvider.DEEPSEEK]:
            return ModelProvider.DEEPSEEK
        elif any(name in model_lower for name in ["llama", "mistral", "mixtral", "qwen"]) or model_lower in SUPPORTED_MODELS[ModelProvider.OLLAMA]:
            return ModelProvider.OLLAMA
        elif model_lower.startswith("databricks") or model_lower in SUPPORTED_MODELS[ModelProvider.DATABRICKS]:
            return ModelProvider.DATABRICKS
            
        # Default to OpenAI for unrecognized models
        return ModelProvider.OPENAI

    @classmethod
    def configure(cls) -> None:
        """Configure the LLM environment with the appropriate settings."""
        # Set up OpenAI client if needed
        if cls._provider != ModelProvider.OLLAMA:
            api_key = cls.get_api_key()
            api_base = cls.get_api_base()
            
            # Set OpenAI global variables for compatibility
            openai.api_key = api_key
            if api_base:
                openai.api_base = api_base
            
            # Set up a client with the retrieved credentials    
            cls._client = OpenAI(
                api_key=api_key,
                base_url=api_base if api_base else None
            )
            logger.info(f"Configured OpenAI client for {cls._provider}")

    @classmethod
    def _configure_env_for_provider(cls, provider: str, model: str, api_key: str, api_base: str) -> None:
        """Configure environment variables for a specific provider."""
        # Set provider-specific environment variables
        if provider == ModelProvider.ANTHROPIC:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        elif provider == ModelProvider.DEEPSEEK:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            # Ensure no /v1 suffix for DeepSeek
            api_base_clean = api_base.rstrip("/v1") if api_base and api_base.endswith("/v1") else api_base
            os.environ["DEEPSEEK_API_BASE"] = api_base_clean or "https://api.deepseek.com"
            # Special config for deepseek-reasoner
            if "deepseek-reasoner" in model:
                os.environ["DEEPSEEK_PREFIX_MESSAGES"] = "true"
        elif provider == ModelProvider.DATABRICKS:
            os.environ["DATABRICKS_TOKEN"] = api_key
            os.environ["DATABRICKS_ENDPOINT"] = api_base or "https://e2-demo-west.cloud.databricks.com/serving-endpoints"
        elif provider == ModelProvider.OLLAMA:
            os.environ["OLLAMA_API_BASE"] = api_base or "http://localhost:11434"
            os.environ["OLLAMA_HOST"] = api_base or "http://localhost:11434"
        else:  # OpenAI
            os.environ["OPENAI_API_KEY"] = api_key
            # Special handling for o-series models
            is_o_series = model and ("o1" in model or "o3" in model or model == "gpt-4o" or model == "gpt-4o-mini")
            if is_o_series:
                os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"

    @classmethod
    def apply_litellm_patch(cls):
        """Apply patches to litellm to ensure it works correctly with our setup."""
        try:
            import litellm
            # Store the original function if we haven't done so already
            if not hasattr(cls, 'original_litellm_completion'):
                cls.original_litellm_completion = litellm.completion
            
            # Apply our patched version
            litellm.completion = cls.patched_litellm_completion
            logger.info("Applied LLMConfig patch to litellm.completion")
        except ImportError:
            logger.warning("Could not import litellm to apply patches")

    @classmethod
    def patch_anthropic_handler(cls):
        """Apply a direct patch to fix the Anthropic API URL in litellm."""
        try:
            import litellm.llms.anthropic.chat.handler as anthropic_handler
            
            # Store the original post_url function if we haven't stored it yet
            if not hasattr(cls, '_original_anthropic_post_url'):
                cls._original_anthropic_post_url = getattr(anthropic_handler, 'post_url', None)
            
            # Define a fixed function that uses the correct URL
            def fixed_post_url(api_base=None, **kwargs):
                # Only apply the fixed URL when the provider is actually Anthropic
                # This prevents issues when switching between providers
                current_provider = cls.get_provider()
                if current_provider == ModelProvider.ANTHROPIC:
                    return "https://api.anthropic.com/v1/messages"
                else:
                    # Use the original function for non-Anthropic providers
                    if cls._original_anthropic_post_url:
                        return cls._original_anthropic_post_url(api_base=api_base, **kwargs)
                    else:
                        # Fallback to a reasonable default
                        return f"{api_base}/chat/completions" if api_base else "https://api.anthropic.com/v1/messages"
            
            # Apply the patch
            setattr(anthropic_handler, 'post_url', fixed_post_url)
            logger.info("Applied provider-specific patch to LiteLLM Anthropic URL")
        except Exception as e:
            logger.warning(f"Failed to patch Anthropic handler: {str(e)}")
            
    @classmethod
    def patch_deepseek_handler(cls):
        """Apply a direct patch to fix the DeepSeek API URL in litellm."""
        try:
            import litellm.llms.deepseek as deepseek_module
            
            # Store the original chat_completion_url function if we haven't stored it yet
            if not hasattr(cls, '_original_deepseek_url'):
                cls._original_deepseek_url = getattr(deepseek_module, 'chat_completion_url', None)
            
            # Define a fixed function that uses the correct URL
            def fixed_url(api_base, model):
                # Only apply the fixed URL when the provider is actually DeepSeek
                current_provider = cls.get_provider()
                if current_provider == ModelProvider.DEEPSEEK:
                    # Ensure base URL doesn't have trailing /v1
                    api_base_clean = api_base.rstrip("/v1") if api_base and api_base.endswith("/v1") else api_base
                    return f"{api_base_clean}/v1/chat/completions"
                else:
                    # Use the original function for non-DeepSeek providers
                    if cls._original_deepseek_url:
                        return cls._original_deepseek_url(api_base, model)
                    else:
                        # Fallback to a reasonable default
                        api_base_clean = api_base.rstrip("/v1") if api_base and api_base.endswith("/v1") else api_base
                        return f"{api_base_clean}/v1/chat/completions"
            
            # Apply the patch
            setattr(deepseek_module, 'chat_completion_url', fixed_url)
            logger.info("Applied provider-specific patch to LiteLLM DeepSeek URL")
        except Exception as e:
            logger.warning(f"Failed to patch DeepSeek handler: {str(e)}")

    @classmethod
    def patch_litellm_transcription(cls):
        """Apply a direct patch to fix the TranscriptionCreateParams issue in litellm."""
        try:
            import litellm
            
            # Check if litellm has the required module
            try:
                from litellm.litellm_core_utils import model_param_helper
                
                # Store the original function
                original_func = getattr(model_param_helper.ModelParamHelper, 
                                       '_get_litellm_supported_transcription_kwargs', None)
                
                # Define a replacement function that doesn't rely on __annotations__
                def patched_get_transcription_kwargs():
                    try:
                        # First try the original function
                        if original_func:
                            return original_func()
                    except Exception:
                        pass
                    
                    # Fallback to hardcoded values
                    return ["file", "model", "response_format", "prompt", "temperature", 
                            "language", "video", "api_base", "api_key"]
                
                # Apply the patch
                if hasattr(model_param_helper, 'ModelParamHelper'):
                    setattr(model_param_helper.ModelParamHelper, 
                           '_get_litellm_supported_transcription_kwargs', 
                           patched_get_transcription_kwargs)
                    logging.info("Applied transcription patch to litellm")
            except ImportError:
                logging.warning("Could not import model_param_helper from litellm.litellm_core_utils. Skipping transcription patch.")
                
        except Exception as e:
            logging.error(f"Failed to patch litellm transcription: {e}")

    @classmethod
    async def configure_litellm_async(cls) -> None:
        """Configure LiteLLM for asynchronous operations."""
        try:
            import litellm
            
            # Set API key and base URL for the current provider
            api_key = await cls.get_api_key_async()
            api_base = cls.get_api_base()
            
            # Set provider-specific environment variables
            provider = cls.get_provider()
            model = cls.get_default_model(provider)
            cls._configure_env_for_provider(provider, model, api_key, api_base)
            
            # Apply necessary patches
            cls.patch_anthropic_handler()
            cls.patch_deepseek_handler()
            cls.patch_litellm_transcription()
            
            # Enable verbose mode for debugging if needed
            # litellm.set_verbose = True
            
            logger.info(f"Configured LiteLLM for async operations with provider: {provider}")
            
        except ImportError:
            logger.error("Could not import litellm for async configuration")
        except Exception as e:
            logger.error(f"Error configuring LiteLLM for async operations: {str(e)}", exc_info=True)

    @classmethod
    def initialize(cls):
        """Initialize the LLMConfig and apply necessary patches."""
        # Configure environment variables and defaults
        cls.configure()
        
        # Apply our patch to litellm.completion
        cls.apply_litellm_patch()
        
        # Apply patch for transcription
        cls.patch_litellm_transcription()
        
        logger.info("LLMConfig initialized with dynamic provider support for mixed model usage")

    @classmethod
    async def generate_async_completion(cls, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 500, db = None):
        """Generate a completion using any model with automatic provider configuration."""
        # Get the model config 
        from .utils.model_config import get_model_config
        model_config = get_model_config(model)
        provider = model_config["provider"]
        
        # Clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=provider)
        
        # Set provider-specific base URLs
        is_o_series = model and ("o1" in model or "o3" in model or model == "gpt-4o" or model == "gpt-4o-mini")
        if provider == ModelProvider.OPENAI and is_o_series:
            cls.set_api_base("https://api.openai.com/v1")
        elif provider == ModelProvider.DEEPSEEK:
            cls.set_api_base("https://api.deepseek.com")  # No /v1 suffix
        elif provider == ModelProvider.ANTHROPIC:
            cls.set_api_base("https://api.anthropic.com")
            # Ensure the Anthropic handler is properly patched
            cls.patch_anthropic_handler()
        
        # Configure for the right provider
        cls.set_provider(provider)
        
        # Initialize database connection if provided
        if db:
            cls.update_db(db)
        
        # Initialize and configure
        cls.initialize()
        await cls.configure_async()
        
        # Get API key and base
        api_key = await cls.get_api_key_async()
        api_base = cls.get_api_base()
        
        logger.info(f"[COMPLETION] Provider: {provider}, Model: {model_config['name']}, API Base: {api_base}")
        
        # Configure environment variables for this provider
        cls._configure_env_for_provider(provider, model, api_key, api_base)
        
        # Handle provider-specific logic
        if provider == ModelProvider.ANTHROPIC:
            # For Anthropic, use their native SDK
            from anthropic import AsyncAnthropic
            from .utils.anthropic_helpers import async_anthropic_completion_with_retry
            
            # Ensure Anthropic API key is properly set
            if api_key == "EMPTY" or not api_key:
                # Try to get from database directly as a last resort
                from .database import SessionLocal
                from .utils.api_key_utils import setup_provider_api_key
                
                try:
                    sync_db = SessionLocal()
                    setup_provider_api_key(sync_db, "ANTHROPIC_API_KEY")
                    sync_db.close()
                    
                    # Verify we have the key now
                    api_key = os.environ.get("ANTHROPIC_API_KEY", "EMPTY")
                    if api_key == "EMPTY" or not api_key:
                        logger.error("Failed to retrieve ANTHROPIC_API_KEY from database")
                        raise ValueError("No valid Anthropic API key found for completion generation")
                    logger.info(f"Retrieved ANTHROPIC_API_KEY from database (key preview: {api_key[:4]}...)")
                except Exception as key_error:
                    logger.error(f"Error retrieving Anthropic API key: {str(key_error)}")
                    raise
                    
            # Log Anthropic authentication details
            logger.info(f"Using Anthropic API key: {api_key[:4]}... for model: {model_config['name']}")
            
            # Extract system message from messages
            system_message = None
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                    # Don't break - use the last system message if multiple exist
                else:
                    user_messages.append(msg)
            
            try:
                # Create Anthropic client and make API call
                anthropic_client = AsyncAnthropic(api_key=api_key)
                
                # Filter messages to the correct format:
                # Anthropic only accepts 'user' and 'assistant' roles
                filtered_messages = []
                for msg in user_messages:
                    role = msg["role"]
                    # Skip system messages as they're handled separately
                    if role == "system":
                        continue
                    # Map 'user' and 'assistant' directly
                    elif role in ["user", "assistant"]:
                        filtered_messages.append({"role": role, "content": msg["content"]})
                    # Map any other roles (like 'function') to 'user'
                    else:
                        filtered_messages.append({"role": "user", "content": msg["content"]})
                
                logger.info(f"Calling Anthropic with model: {model_config['name']}")
                logger.info(f"System message: {system_message}")
                logger.info(f"Number of messages: {len(filtered_messages)}")
                
                # Get the max_rpm setting from the model configuration
                max_rpm = model_config.get("max_rpm", 3)  # Default to 3 RPM if not specified
                logger.info(f"Using max_rpm={max_rpm} for Anthropic API call")
                
                # Use our async retry helper function for Anthropic API calls
                response = await async_anthropic_completion_with_retry(
                    anthropic_client,
                    model=model_config["name"],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_message,
                    messages=filtered_messages,
                    rpm=max_rpm  # Pass the max_rpm setting to the retry helper
                )
                
                # Convert to OpenAI-compatible format
                return {
                    "choices": [{"message": {"content": response.content[0].text}}]
                }
            except Exception as e:
                logger.error(f"Error calling Anthropic API: {str(e)}")
                # Log detailed error information
                import traceback
                logger.error(f"Detailed error: {traceback.format_exc()}")
                raise ValueError(f"Anthropic API error: {str(e)}")
        else:
            # For all other providers, use LiteLLM
            try:
                # Prepare model name with provider prefix if needed
                model_name = model_config["name"]
                
                if provider in [ModelProvider.DATABRICKS, ModelProvider.OLLAMA]:
                    model_name = f"{provider}/{model_name}"
                elif provider == ModelProvider.DEEPSEEK and not model_name.startswith("deepseek/"):
                    model_name = f"deepseek/{model_name}"
                
                # Build completion parameters
                completion_params = {
                    "model": model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                
                # Add API key if it exists and is needed
                if api_key != "EMPTY":
                    completion_params["api_key"] = api_key
                
                # Add API base with appropriate cleaning
                if api_base:
                    if provider == ModelProvider.DEEPSEEK and api_base.endswith("/v1"):
                        completion_params["api_base"] = api_base.rstrip("/v1")
                    else:
                        completion_params["api_base"] = api_base
                
                # Add provider for non-OpenAI APIs
                if provider != ModelProvider.OPENAI:
                    completion_params["provider"] = str(provider).replace("ModelProvider.", "").lower()
                
                # For O-series models, ensure correct base URL
                if provider == ModelProvider.OPENAI and is_o_series:
                    completion_params["api_base"] = "https://api.openai.com/v1"
                
                # Make the API call
                return await litellm.acompletion(**completion_params)
                
            except Exception as e:
                logger.error(f"Error in LiteLLM completion: {str(e)}")
                logger.exception("Full traceback:")
                raise

    @classmethod
    def get_model_name_for_crewai(cls, model: str = None) -> str:
        """Get the properly formatted model name for CrewAI."""
        if not model:
            model = cls.get_default_model()
            
        # Detect provider based on model name
        provider = cls._detect_provider_from_model(model)
        
        # Configure environment for each provider
        if provider == ModelProvider.OPENAI:
            cls.setup_openai_for_agent()
            # Special handling for o-series models
            is_o_series = model and ("o1" in model or "o3" in model or model == "gpt-4o" or model == "gpt-4o-mini")
            if is_o_series:
                os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"
                
        elif provider == ModelProvider.DEEPSEEK:
            cls.setup_deepseek_for_agent()
            # CRITICAL: ADD the 'deepseek/' prefix to ensure LiteLLM can identify the provider
            # This is necessary for LiteLLM to route the model correctly
            if not model.startswith("deepseek/"):
                model = f"deepseek/{model}"
                logger.info(f"Added 'deepseek/' prefix to model for CrewAI: {model}")
                
        elif provider == ModelProvider.ANTHROPIC:
            cls.setup_anthropic_for_agent()
            # CRITICAL: Do NOT add the 'anthropic/' prefix
            # LiteLLM needs the raw model name without prefix for Anthropic
            # This allows the provider to be correctly detected by our patched function
            # Ensure any existing prefix is removed
            if model.startswith("anthropic/"):
                model = model[len("anthropic/"):]
                
        elif provider == ModelProvider.OLLAMA:
            cls.setup_ollama_for_agent()
            
        elif provider == ModelProvider.DATABRICKS:
            cls.setup_databricks_for_agent()
            # Add provider prefix if needed
            if not model.startswith("databricks/"):
                model = f"databricks/{model}"
                
        return model

    @classmethod
    def setup_anthropic_for_agent(cls) -> None:
        """Set up Anthropic-specific configuration for an agent using Claude models."""
        # First clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=ModelProvider.ANTHROPIC)
        
        from .database import SessionLocal
        from .utils.api_key_utils import setup_provider_api_key
        
        try:
            # Set up the Anthropic API key directly from database
            db = SessionLocal()
            success = setup_provider_api_key(db, "ANTHROPIC_API_KEY")
            db.close()
            
            if success:
                logger.info("Successfully set up Anthropic API key from database")
                
                # Set proper API base URL
                os.environ["ANTHROPIC_API_BASE"] = "https://api.anthropic.com"
                
                # Remove any variables that might interfere with Anthropic API calls
                for var in ["LITELLM_FORCE_COMPLETION_URL", "LITELLM_PROVIDER"]:
                    if var in os.environ:
                        os.environ.pop(var, None)
                        logger.info(f"Removed {var} from environment to prevent conflicts with Anthropic API")
                
                # Make sure we have no OpenAI base URL to avoid confusion
                os.environ["OPENAI_API_BASE"] = ""
                
                # Verify the API key 
                api_key = os.environ.get("ANTHROPIC_API_KEY", "")
                if api_key and len(api_key) > 8:
                    logger.info(f"Verified Anthropic API key (starts with {api_key[:4]}...)")
                else:
                    logger.warning(f"Anthropic API key may be invalid: {api_key[:4] if api_key else 'None'}")
                    
                logger.info("Set ANTHROPIC_API_BASE to: https://api.anthropic.com")
            else:
                logger.warning("Failed to set up Anthropic API key from database")
        except Exception as e:
            logger.error(f"Error setting up Anthropic API key: {str(e)}")
    
    @classmethod
    def setup_openai_for_agent(cls) -> None:
        """Set up OpenAI-specific configuration for an agent."""
        # First clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=ModelProvider.OPENAI)
        
        from .database import SessionLocal
        from .utils.api_key_utils import setup_provider_api_key
        
        try:
            # Set up the OpenAI API key directly from database
            db = SessionLocal()
            success = setup_provider_api_key(db, "OPENAI_API_KEY")
            db.close()
            
            if success:
                logger.info("Successfully set up OpenAI API key from database")
            else:
                logger.warning("Failed to set up OpenAI API key from database")
        except Exception as e:
            logger.error(f"Error setting up OpenAI API key: {str(e)}")
    
    @classmethod
    def setup_deepseek_for_agent(cls) -> None:
        """Set up DeepSeek-specific configuration for an agent."""
        # First clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=ModelProvider.DEEPSEEK)
        
        from .database import SessionLocal
        from .utils.api_key_utils import setup_provider_api_key
        
        try:
            # Set up the DeepSeek API key directly from database
            db = SessionLocal()
            success = setup_provider_api_key(db, "DEEPSEEK_API_KEY")
            db.close()
            
            if success:
                logger.info("Successfully set up DeepSeek API key from database")
                
                # CRITICAL: Make sure OpenAI API base is completely unset
                if "OPENAI_API_BASE" in os.environ:
                    os.environ.pop("OPENAI_API_BASE")
                    logger.info("Cleared OPENAI_API_BASE to prevent conflicts with DeepSeek")
                
                # Set proper API base URL (without /v1 suffix)
                os.environ["DEEPSEEK_API_BASE"] = "https://api.deepseek.com"
                logger.info(f"Set DEEPSEEK_API_BASE to: https://api.deepseek.com")
                
                # Remove any force completion URL to let LiteLLM determine it from model name
                if "LITELLM_FORCE_COMPLETION_URL" in os.environ:
                    os.environ.pop("LITELLM_FORCE_COMPLETION_URL")
                    logger.info("Removed LITELLM_FORCE_COMPLETION_URL to let LiteLLM handle provider detection")
                
                # Remove any environment variables that might interfere with provider detection
                for var in ["LITELLM_PROVIDER"]:
                    if var in os.environ:
                        os.environ.pop(var, None)
                        logger.info(f"Removed {var} from environment to ensure proper provider detection")
                
                # Verify the API key 
                api_key = os.environ.get("DEEPSEEK_API_KEY", "")
                if api_key and len(api_key) > 8:
                    logger.info(f"Verified DeepSeek API key (starts with {api_key[:4]}...)")
                else:
                    logger.warning(f"DeepSeek API key may be invalid: {api_key[:4] if api_key else 'None'}")
            else:
                logger.warning("Failed to set up DeepSeek API key from database")
        except Exception as e:
            logger.error(f"Error setting up DeepSeek API key: {str(e)}")
            
    @classmethod
    def setup_databricks_for_agent(cls) -> None:
        """Set up Databricks-specific configuration for an agent."""
        # First clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=ModelProvider.DATABRICKS)
        
        from .database import SessionLocal
        from .utils.api_key_utils import setup_provider_api_key
        
        try:
            # Set up the Databricks token directly from database
            db = SessionLocal()
            success = setup_provider_api_key(db, "DATABRICKS_TOKEN")
            db.close()
            
            if success:
                logger.info("Successfully set up Databricks token from database")
                
                # Set proper API endpoint
                api_base = cls.get_api_base()
                os.environ["DATABRICKS_ENDPOINT"] = api_base or "https://e2-demo-west.cloud.databricks.com/serving-endpoints"
            else:
                logger.warning("Failed to set up Databricks token from database")
        except Exception as e:
            logger.error(f"Error setting up Databricks token: {str(e)}")
            
    @classmethod
    def setup_ollama_for_agent(cls) -> None:
        """Set up Ollama-specific configuration for an agent."""
        # First clear any other provider environment variables to prevent conflicts
        cls._clear_provider_environments(except_provider=ModelProvider.OLLAMA)
        
        api_base = cls.get_api_base()
        os.environ["OLLAMA_API_BASE"] = api_base or "http://localhost:11434"
        os.environ["OLLAMA_HOST"] = api_base or "http://localhost:11434"
        logger.info(f"Set up Ollama with API base: {os.environ['OLLAMA_API_BASE']}")

    @classmethod
    def _clear_provider_environments(cls, except_provider=None):
        """Clear environment variables for other providers to prevent conflicts."""
        env_vars_to_clear = {
            ModelProvider.OPENAI: ["OPENAI_API_BASE"],
            ModelProvider.ANTHROPIC: ["ANTHROPIC_API_BASE"],
            ModelProvider.DEEPSEEK: ["DEEPSEEK_API_BASE", "DEEPSEEK_PREFIX_MESSAGES"],
            ModelProvider.DATABRICKS: ["DATABRICKS_ENDPOINT"],
            ModelProvider.OLLAMA: ["OLLAMA_API_BASE", "OLLAMA_HOST"]
        }
        
        # Skip the excepted provider
        if except_provider:
            env_vars_to_clear.pop(except_provider, None)
            
        # Clear the environment variables
        for provider, vars_list in env_vars_to_clear.items():
            for var in vars_list:
                if var in os.environ:
                    logger.info(f"Clearing {var} to prevent conflicts with {except_provider}")
                    os.environ.pop(var, None)

    @staticmethod
    def patched_litellm_completion(model, messages, **kwargs):
        """Patched version of litellm.completion that ensures proper environment setup."""
        if not hasattr(LLMConfig, 'original_litellm_completion'):
            import litellm
            LLMConfig.original_litellm_completion = litellm.completion

        # Make sure we have the original function
        original_litellm_completion = LLMConfig.original_litellm_completion
        
        # Special handling for DeepSeek models with other providers
        if model and ('deepseek' in model or model in SUPPORTED_MODELS.get(ModelProvider.DEEPSEEK, [])):
            # CRITICAL: Keep the "deepseek/" prefix if it exists, add it if it doesn't
            # LiteLLM relies on this prefix to properly route the request
            if isinstance(model, str) and not model.startswith("deepseek/"):
                model = f"deepseek/{model}"
                logging.info(f"Added 'deepseek/' prefix to model name: {model}")
            
            # Ensure we're using the DeepSeek provider for this call
            api_key = os.getenv("DEEPSEEK_API_KEY", "")
            if api_key:
                kwargs['api_key'] = api_key
            
            # CRITICAL: Force the correct API base
            kwargs['api_base'] = "https://api.deepseek.com"
            
            # Force the completion URL to use the correct endpoint
            kwargs['force_completion_url'] = "https://api.deepseek.com/v1/chat/completions"
            
            # Do NOT explicitly set provider here since LiteLLM will determine it from the model name prefix
            # Remove provider if it's already set to avoid overriding LiteLLM's detection
            if 'provider' in kwargs:
                kwargs.pop('provider')
            
            # Clear any conflicting OpenAI settings
            for key in ['model_response_format', 'seed', 'function_call', 'functions', 'tools']:
                if key in kwargs:
                    kwargs.pop(key)
            
            logging.info(f"DeepSeek API configuration: api_base={kwargs['api_base']}, url={kwargs['force_completion_url']}")
            
        # Special handling for Anthropic models with other providers
        elif model and ('claude' in model or model in SUPPORTED_MODELS.get(ModelProvider.ANTHROPIC, [])):
            # CRITICAL: Remove any prefix from model name - Claude models should not have 'anthropic/' prefix
            if isinstance(model, str) and '/' in model:
                prefix, model_name = model.split('/', 1)
                if prefix.lower() == 'anthropic':
                    model = model_name
                    logging.info(f"Removed 'anthropic/' prefix from model name, using: {model}")
            
            # Get API key directly from env variable
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            if api_key:
                kwargs['api_key'] = api_key
            
            # Set base URL for Anthropic
            kwargs['api_base'] = "https://api.anthropic.com"
            
            # Extract system message from messages
            system_message = None
            filtered_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    filtered_messages.append(msg)
            
            # Add system message as a separate parameter for Anthropic
            if system_message:
                kwargs['system'] = system_message
                # Override messages to exclude system message
                messages = [msg for msg in filtered_messages]
            
            # Adjust parameters for compatibility with Anthropic API
            if 'temperature' in kwargs:
                temperature = kwargs['temperature']
                # Anthropic temperature is capped at 1.0
                kwargs['temperature'] = min(float(temperature), 1.0)
            
            if 'max_tokens' in kwargs:
                kwargs['max_tokens_to_sample'] = kwargs.pop('max_tokens')
            
            # Remove any potentially problematic parameters
            # A cleaner and more targeted approach
            problematic_params = [
                'provider', 'custom_llm_provider', 'litellm_params', 'completion_mode',
                'model_response_format', 'seed', 'function_call', 'functions', 'tools',
                'force_completion_url', 'stream', 'top_p', 'frequency_penalty',
                'presence_penalty', 'best_of', 'n', 'logprobs'
            ]
            
            for param in problematic_params:
                if param in kwargs:
                    param_value = kwargs.pop(param)
                    logging.info(f"Removed {param}={param_value} for Anthropic API compatibility")
        
        # Log the actual API call for debugging
        logging.info(f"LiteLLM completion() model={model}")
        logging.info(f"Parameters: {', '.join(f'{k}={v}' for k, v in kwargs.items() if not isinstance(v, dict) and not k == 'api_key')}")
        
        try:
            # Add helpful debug information
            if 'claude' in model or model in SUPPORTED_MODELS.get(ModelProvider.ANTHROPIC, []):
                import litellm
                # Enable debug mode if Anthropic model
                litellm.set_verbose = True
                logging.info(f"Calling Anthropic with model={model}, system={kwargs.get('system', 'None')}")
            
            # Enable debug for DeepSeek
            if 'deepseek' in model or model in SUPPORTED_MODELS.get(ModelProvider.DEEPSEEK, []):
                import litellm
                litellm.set_verbose = True
                logging.info(f"Calling DeepSeek with model={model}, api_base={kwargs.get('api_base')}")
            
            # Use try/except to help diagnose any issues
            return original_litellm_completion(model, messages, **kwargs)
        except Exception as e:
            logging.error(f"Error in LiteLLM completion: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                logging.error(f"Response error details: {e.response.text}")
            raise
