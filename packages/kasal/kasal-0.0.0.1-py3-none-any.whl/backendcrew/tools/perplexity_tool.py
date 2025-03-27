from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field, PrivateAttr
import logging
import requests

# Configure logger
logger = logging.getLogger(__name__)

# Input schema for PerplexitySearchTool
class PerplexitySearchInput(BaseModel):
    """Input schema for PerplexitySearchTool."""
    query: str = Field(..., description="The search query or question to pass to Perplexity AI.")

class PerplexitySearchTool(BaseTool):
    name: str = "PerplexityTool"
    description: str = (
        "A tool that performs web searches using Perplexity AI to find accurate and up-to-date information. "
        "Input should be a specific search query or question."
    )
    args_schema: Type[BaseModel] = PerplexitySearchInput
    _api_key: Optional[str] = PrivateAttr(default=None)

    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        if not api_key:
            api_key = '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'
        self._api_key = api_key
        logger.info(f"Initialized Perplexity tool with API key: {'*' * len(api_key)}")

    def _run(self, query: str) -> str:
        """
        Execute a search query using the Perplexity API directly.
        """
        try:
            url = "https://api.perplexity.ai/chat/completions"
            
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and concise."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.1,
                "top_p": 0.9,
                "search_domain_filter": ["perplexity.ai"],
                "return_images": False,
                "return_related_questions": False,
                "search_recency_filter": "month",
                "top_k": 0,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 1
            }
            
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }

            logger.info(f"Executing Perplexity API request with query: {query}")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes
            
            result = response.json()
            answer = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            logger.info(f"Perplexity answer: {answer}")
            return answer

        except Exception as e:
            error_msg = f"Error executing Perplexity API request: {str(e)}"
            logger.error(error_msg)
            return error_msg