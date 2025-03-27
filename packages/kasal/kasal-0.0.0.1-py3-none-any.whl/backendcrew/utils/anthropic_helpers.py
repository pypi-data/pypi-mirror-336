import time
import logging
import asyncio
from anthropic import Anthropic, AsyncAnthropic, RateLimitError, APIError, APITimeoutError
from typing import Dict, Any, Optional, List, Callable, Union
from .token_bucket import consume_anthropic_input_tokens, consume_anthropic_output_tokens

logger = logging.getLogger(__name__)

def call_with_retry(func: Callable, *args: Any, max_retries: int = 5, initial_backoff: float = 2.0, rpm: Optional[int] = None, **kwargs: Any) -> Any:
    """
    Call an Anthropic API function with exponential backoff retry logic.
    
    Args:
        func: The Anthropic API function to call
        *args: Arguments to pass to the function
        max_retries: Maximum number of retries before giving up
        initial_backoff: Initial backoff time in seconds
        rpm: Optional max RPM setting for rate limiting
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the function call
        
    Raises:
        The last exception encountered if all retries fail
    """
    backoff_time = initial_backoff
    last_exception = None
    
    # Estimate input token count based on messages
    # This is a simple estimator - in production, you'd use a proper tokenizer
    messages = kwargs.get('messages', [])
    system = kwargs.get('system', '')
    estimated_input_tokens = 0
    
    # Count system message tokens (very rough estimate)
    if system:
        estimated_input_tokens += len(system.split()) * 1.3
    
    # Count message tokens (very rough estimate)
    for msg in messages:
        content = msg.get('content', '')
        if isinstance(content, str):
            estimated_input_tokens += len(content.split()) * 1.3
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    estimated_input_tokens += len(item['text'].split()) * 1.3
    
    # Estimate is in words, convert to tokens (very rough approximation)
    estimated_input_tokens = int(estimated_input_tokens)
    
    # Get max_tokens (estimated output tokens)
    estimated_output_tokens = kwargs.get('max_tokens', 1000)
    
    logger.info(f"Estimated input tokens: {estimated_input_tokens}, output tokens: {estimated_output_tokens}")
    
    # Apply token bucket rate limiting for input tokens
    if not consume_anthropic_input_tokens(estimated_input_tokens, wait=True, rpm=rpm):
        logger.warning("Failed to consume input tokens from token bucket")
    
    # Apply token bucket rate limiting for output tokens
    if not consume_anthropic_output_tokens(estimated_output_tokens, wait=True, rpm=rpm):
        logger.warning("Failed to consume output tokens from token bucket")
    
    for retry in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            last_exception = e
            if retry == max_retries:
                logger.error(f"Rate limit exceeded after {max_retries} retries: {e}")
                raise
            
            # Extract retry_after from response if available
            retry_after = getattr(e, "retry_after", None)
            if retry_after is not None:
                backoff_time = float(retry_after)
            else:
                backoff_time = initial_backoff * (2 ** retry)
                
            logger.warning(f"Rate limit hit. Retrying in {backoff_time:.2f}s... (Attempt {retry+1}/{max_retries})")
            time.sleep(backoff_time)
        except (APIError, APITimeoutError) as e:
            last_exception = e
            if retry == max_retries:
                logger.error(f"API error after {max_retries} retries: {e}")
                raise
                
            backoff_time = initial_backoff * (2 ** retry)
            logger.warning(f"API error: {e}. Retrying in {backoff_time:.2f}s... (Attempt {retry+1}/{max_retries})")
            time.sleep(backoff_time)
            
    # This should never be reached due to the raise in the last iteration
    if last_exception:
        raise last_exception
    return None

async def async_call_with_retry(func: Callable, *args: Any, max_retries: int = 5, initial_backoff: float = 2.0, rpm: Optional[int] = None, **kwargs: Any) -> Any:
    """
    Async version: Call an Anthropic API function with exponential backoff retry logic.
    
    Args:
        func: The async Anthropic API function to call
        *args: Arguments to pass to the function
        max_retries: Maximum number of retries before giving up
        initial_backoff: Initial backoff time in seconds
        rpm: Optional max RPM setting for rate limiting
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        The result of the function call
        
    Raises:
        The last exception encountered if all retries fail
    """
    backoff_time = initial_backoff
    last_exception = None
    
    # Estimate input token count based on messages
    # This is a simple estimator - in production, you'd use a proper tokenizer
    messages = kwargs.get('messages', [])
    system = kwargs.get('system', '')
    estimated_input_tokens = 0
    
    # Count system message tokens (very rough estimate)
    if system:
        estimated_input_tokens += len(system.split()) * 1.3
    
    # Count message tokens (very rough estimate)
    for msg in messages:
        content = msg.get('content', '')
        if isinstance(content, str):
            estimated_input_tokens += len(content.split()) * 1.3
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    estimated_input_tokens += len(item['text'].split()) * 1.3
    
    # Estimate is in words, convert to tokens (very rough approximation)
    estimated_input_tokens = int(estimated_input_tokens)
    
    # Get max_tokens (estimated output tokens)
    estimated_output_tokens = kwargs.get('max_tokens', 1000)
    
    logger.info(f"Estimated input tokens: {estimated_input_tokens}, output tokens: {estimated_output_tokens}")
    
    # Apply token bucket rate limiting for input tokens
    if not consume_anthropic_input_tokens(estimated_input_tokens, wait=True, rpm=rpm):
        logger.warning("Failed to consume input tokens from token bucket")
    
    # Apply token bucket rate limiting for output tokens
    if not consume_anthropic_output_tokens(estimated_output_tokens, wait=True, rpm=rpm):
        logger.warning("Failed to consume output tokens from token bucket")
    
    for retry in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except RateLimitError as e:
            last_exception = e
            if retry == max_retries:
                logger.error(f"Rate limit exceeded after {max_retries} retries: {e}")
                raise
            
            # Extract retry_after from response if available
            retry_after = getattr(e, "retry_after", None)
            if retry_after is not None:
                backoff_time = float(retry_after)
            else:
                backoff_time = initial_backoff * (2 ** retry)
                
            logger.warning(f"Rate limit hit. Retrying in {backoff_time:.2f}s... (Attempt {retry+1}/{max_retries})")
            await asyncio.sleep(backoff_time)
        except (APIError, APITimeoutError) as e:
            last_exception = e
            if retry == max_retries:
                logger.error(f"API error after {max_retries} retries: {e}")
                raise
                
            backoff_time = initial_backoff * (2 ** retry)
            logger.warning(f"API error: {e}. Retrying in {backoff_time:.2f}s... (Attempt {retry+1}/{max_retries})")
            await asyncio.sleep(backoff_time)
            
    # This should never be reached due to the raise in the last iteration
    if last_exception:
        raise last_exception
    return None

# Exported helpers for use in other parts of the application
def create_anthropic_client(api_key: Optional[str] = None, **kwargs: Any) -> Anthropic:
    """Create an Anthropic client with the provided API key."""
    return Anthropic(api_key=api_key, **kwargs)

def create_async_anthropic_client(api_key: Optional[str] = None, **kwargs: Any) -> AsyncAnthropic:
    """Create an async Anthropic client with the provided API key."""
    return AsyncAnthropic(api_key=api_key, **kwargs)

def anthropic_completion_with_retry(
    client: Anthropic,
    *args: Any,
    max_retries: int = 5,
    rpm: Optional[int] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Call Anthropic's completion API with retry logic
    """
    return call_with_retry(client.messages.create, *args, max_retries=max_retries, rpm=rpm, **kwargs)

async def async_anthropic_completion_with_retry(
    client: AsyncAnthropic,
    *args: Any,
    max_retries: int = 5,
    rpm: Optional[int] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Call Anthropic's completion API with retry logic (async version)
    """
    return await async_call_with_retry(client.messages.create, *args, max_retries=max_retries, rpm=rpm, **kwargs) 