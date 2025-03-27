"""
Utility module for model configurations.
"""

def get_model_config(model: str) -> dict:
    """
    Get the configuration for different AI models.
    
    Args:
        model (str): The model identifier
        
    Returns:
        dict: Model configuration containing name, temperature and provider
    """
    models = {
        "gpt-4-turbo": {
            "name": "gpt-4-turbo-preview",
            "temperature": 0.7,
            "provider": "openai"
        },
        "gpt-4": {
            "name": "gpt-4",
            "temperature": 0.7,
            "provider": "openai"
        },
        "gpt-4o-mini": {
            "name": "gpt-4o-mini",
            "temperature": 0.7,
            "provider": "openai"
        },
        "o1-preview": {
            "name": "o1-preview",
            "temperature": 1,
            "provider": "openai"
        },
        "o1": {
            "name": "o1",
            "temperature": 1,
            "provider": "openai"
        },
        "o1-mini": {
            "name": "o1-mini",
            "temperature": 1,
            "provider": "openai"
        },
        "o3": {
            "name": "o3",
            "temperature": 1,
            "provider": "openai"
        },
        "o3-mini": {
            "name": "o3-mini",
            "temperature": 1,
            "provider": "openai"
        },
        "o3-mini-high": {
            "name": "o3-mini-high",
            "temperature": 1,
            "provider": "openai"
        },
        "gpt-4o": {
            "name": "gpt-4o",
            "temperature": 0.7,
            "provider": "openai"
        },
        "gpt-3.5-turbo": {
            "name": "gpt-3.5-turbo",
            "temperature": 0.7,
            "provider": "openai"
        },
        "claude-3-5-sonnet-20241022": {
            "name": "claude-3-5-sonnet-20241022",
            "temperature": 0.7,
            "provider": "anthropic"
        },
        "claude-3-5-haiku-20241022": {
            "name": "claude-3-5-haiku-20241022",
            "temperature": 0.7,
            "provider": "anthropic"
        },
        "claude-3-7-sonnet-20250219": {
            "name": "claude-3-7-sonnet-20250219",
            "temperature": 0.7,
            "provider": "anthropic"
        },
        "claude-3-7-sonnet-20250219-thinking": {
            "name": "claude-3-7-sonnet-20250219",
            "temperature": 0.7,
            "provider": "anthropic",
            "extended_thinking": True
        },
        "claude-3-opus-20240229": {
            "name": "claude-3-opus-20240229",
            "temperature": 0.7,
            "provider": "anthropic"
        },
        "llama2:13b": {
            "name": "llama2:13b",
            "temperature": 0.7,
            "provider": "ollama"
        },
        "deepseek-chat": {
            "name": "deepseek-chat",
            "temperature": 0.7,
            "provider": "deepseek"
        },
        "deepseek-reasoner": {
            "name": "deepseek-reasoner", 
            "temperature": 0.7,
            "provider": "deepseek"
        },
        "qwen2.5:32b": {
            "name": "qwen2.5:32b",
            "temperature": 0.7,
            "provider": "ollama"
        },
        "databricks-meta-llama-3-3-70b-instruct": {
            "name": "databricks-meta-llama-3-3-70b-instruct",
            "temperature": 0.7,
            "provider": "databricks"
        },
        "databricks-meta-llama-3-1-405b-instruct": {
            "name": "databricks-meta-llama-3-1-405b-instruct",
            "temperature": 0.7,
            "provider": "databricks"
        }
    }
    return models.get(model, models["gpt-4-turbo"])  # Default to gpt-4-turbo if model not found 