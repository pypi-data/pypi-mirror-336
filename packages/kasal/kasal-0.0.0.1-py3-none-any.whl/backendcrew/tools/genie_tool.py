from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field, PrivateAttr
import logging
import requests
import json
import time
import os
import base64
import sqlite3
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)

class GenieInput(BaseModel):
    """Input schema for Genie."""
    question: str = Field(..., description="The question to be answered using Genie.")

def get_access_token(
    workspace_url: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None
) -> dict:
    """
    Get access token from Databricks using client credentials.
    
    Args:
        workspace_url: The Databricks workspace URL
        client_id: The client ID (if not provided, will look for DATABRICKS_CLIENT_ID env var)
        client_secret: The client secret (if not provided, will look for CLIENT_SECRET env var)
    
    Returns:
        dict: The response JSON containing the access token and other details
    """
    # Get credentials from environment variables if not provided
    client_id = client_id or os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = client_secret or os.getenv("DATABRICKS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("DATABRICKS_CLIENT_ID and DATABRICKS_CLIENT_SECRET must be provided either as arguments or environment variables")

    # Create the Basic auth header manually
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('ascii')
    base64_auth = base64.b64encode(auth_bytes).decode('ascii')
    
    # Construct the token endpoint URL
    token_endpoint = f"{workspace_url}/oidc/v1/token"
    
    headers = {
        'Authorization': f'Basic {base64_auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(
        token_endpoint,
        headers=headers,
        data="grant_type=client_credentials&scope=all-apis"
    )
    
    # Raise an exception for bad responses
    response.raise_for_status()
    
    return response.json()

class GenieTool(BaseTool):
    name: str = "GenieTool"
    description: str = (
        "A tool that uses Genie to find information about customers and business data. "
        "Input should be a specific business question."
    )
    args_schema: Type[BaseModel] = GenieInput
    _host: str = PrivateAttr(default=None)
    _client_id: str = PrivateAttr(default=None)
    _client_secret: str = PrivateAttr(default=None)
    _space_id: str = PrivateAttr(default=None)
    _max_retries: int = PrivateAttr(default=60)
    _retry_delay: int = PrivateAttr(default=5)
    _current_conversation_id: str = PrivateAttr(default=None)
    _token: str = PrivateAttr(default=None)
    _tool_id: int = PrivateAttr(default=35)  # Default tool ID

    def __init__(self, tool_config: Optional[dict] = None, tool_id: Optional[int] = None):
        super().__init__()
        if tool_config is None:
            tool_config = {}
            
        # Set tool ID if provided
        if tool_id is not None:
            self._tool_id = tool_id

        # Get the database path
        package_dir = Path(__file__).resolve().parent.parent
        db_path = str(package_dir / 'crewai.db')
        
        try:
            # Connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query the tools table for GenieTool configuration
            cursor.execute("""
                SELECT config
                FROM tools 
                WHERE title = 'GenieTool' AND id = ?
            """, (self._tool_id,))
            
            result = cursor.fetchone()
            if result and result[0]:
                db_config = json.loads(result[0])
                # Update tool_config with database values, but don't override provided values
                for key, value in db_config.items():
                    if key not in tool_config:
                        tool_config[key] = value
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error fetching GenieTool config from database: {str(e)}")
            # Continue with default values if database access fails
        
        # Initialize basic configuration
        self._host = os.getenv("DATABRICKS_HOST", "e2-demo-field-eng.cloud.databricks.com")
        self._space_id = tool_config.get('spaceId', "01efcca6fdc712d7be87a40ad4a2e33e")
        self._client_id = tool_config.get('client_id') or os.getenv("DATABRICKS_CLIENT_ID")
        self._client_secret = tool_config.get('client_secret') or os.getenv("DATABRICKS_CLIENT_SECRET")
        
        if not self._client_id or not self._client_secret:
            raise ValueError("DATABRICKS_CLIENT_ID and DATABRICKS_CLIENT_SECRET must be provided either in tool_config or as environment variables")

        if not self._host:
            raise ValueError("DATABRICKS_HOST must be provided in environment variables")

        # Get the access token
        workspace_url = f"https://{self._host}"
        token_response = get_access_token(workspace_url, self._client_id, self._client_secret)
        self._token = token_response.get("access_token")
        
        if not self._token:
            raise ValueError("Failed to obtain access token")
            
        # Log successful token acquisition
        logger.info("Successfully obtained access token!")
        masked_token = f"{self._token[:8]}...{self._token[-8:]}" if len(self._token) > 16 else "***"
        logger.info(f"Token (masked): {masked_token}")
        logger.info(f"Token expires in: {token_response.get('expires_in', 'N/A')} seconds")
        
        # Add detailed debugging logs
        logger.info("GenieTool Configuration:")
        logger.info(f"Tool ID: {self._tool_id}")
        logger.info(f"Host: {self._host}")
        logger.info(f"Space ID: {self._space_id}")
        # Mask credentials for security
        masked_client_id = f"{self._client_id[:4]}...{self._client_id[-4:]}" if len(self._client_id) > 8 else "***"
        logger.info(f"Client ID (masked): {masked_client_id}")
        
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
        })

    def _make_url(self, path: str) -> str:
        """Create a full URL from a path."""
        return f"https://{self._host.rstrip('/')}/{path.lstrip('/')}"

    def _start_or_continue_conversation(self, question: str) -> dict:
        """Start a new conversation or continue existing one with a question."""
        try:
            if self._current_conversation_id:
                # Continue existing conversation
                url = self._make_url(f"api/2.0/genie/spaces/{self._space_id}/conversations/{self._current_conversation_id}/messages")
                payload = {"content": question}
                response = self._session.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                message_id = data.get("message_id") or data.get("id")
                return {
                    "conversation_id": self._current_conversation_id,
                    "message_id": message_id
                }
            else:
                # Start new conversation
                url = self._make_url(f"api/2.0/genie/spaces/{self._space_id}/start-conversation")
                payload = {"content": question}
                logger.info(f"Starting new conversation with URL: {url}")
                logger.info(f"Payload: {payload}")
                response = self._session.post(url, json=payload)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTP Error: {str(e)}")
                    logger.error(f"Response status: {response.status_code}")
                    logger.error(f"Response body: {response.text}")
                    raise
                data = response.json()
                self._current_conversation_id = data.get("conversation_id")
                message_id = data.get("message_id") or data.get("id")
                return {
                    "conversation_id": self._current_conversation_id,
                    "message_id": message_id
                }
        except Exception as e:
            logger.error(f"Error in _start_or_continue_conversation: {str(e)}")
            raise

    def _get_message_status(self, conversation_id: str, message_id: str) -> dict:
        """Get the status and content of a message."""
        url = self._make_url(
            f"api/2.0/genie/spaces/{self._space_id}/conversations/{conversation_id}/messages/{message_id}"
        )
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def _get_query_result(self, conversation_id: str, message_id: str) -> dict:
        """Get the SQL query results for a message."""
        url = self._make_url(
            f"api/2.0/genie/spaces/{self._space_id}/conversations/{conversation_id}/messages/{message_id}/query-result"
        )
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def _extract_response(self, message_status: dict, result_data: Optional[dict] = None) -> str:
        """Extract the response from message status and query results."""
        response_parts = []
        
        # Extract text response
        text_response = ""
        if "attachments" in message_status:
            for attachment in message_status["attachments"]:
                if "text" in attachment and attachment["text"].get("content"):
                    text_response = attachment["text"]["content"]
                    break
        
        if not text_response:
            for field in ["content", "response", "answer", "text"]:
                if message_status.get(field):
                    text_response = message_status[field]
                    break
        
        # Add text response if it's meaningful (not empty and not just echoing the question)
        if text_response.strip() and text_response.strip() != message_status.get("content", "").strip():
            response_parts.append(text_response)
        
        # Process query results if available
        if result_data and "statement_response" in result_data:
            result = result_data["statement_response"].get("result", {})
            if "data_typed_array" in result and result["data_typed_array"]:
                data_array = result["data_typed_array"]
                
                # If no meaningful text response but we have data, add a summary
                if not response_parts:
                    response_parts.append(f"Query returned {len(data_array)} rows.")
                
                response_parts.append("\nQuery Results:")
                response_parts.append("-" * 20)
                
                # Format the results in a table
                if data_array:
                    first_row = data_array[0]
                    # Calculate column widths
                    widths = []
                    for i in range(len(first_row["values"])):
                        col_values = [str(row["values"][i].get("str", "")) for row in data_array]
                        max_width = max(len(val) for val in col_values) + 2
                        widths.append(max_width)
                    
                    # Format and add each row
                    for row in data_array:
                        row_values = []
                        for i, value in enumerate(row["values"]):
                            row_values.append(f"{value.get('str', ''):<{widths[i]}}")
                        response_parts.append("".join(row_values))
                
                response_parts.append("-" * 20)
        
        return "\n".join(response_parts) if response_parts else "No response content found"

    def _run(self, question: str) -> str:
        """
        Execute a query using the Genie API and wait for results.
        """
        try:
            # Start or continue conversation
            conv_data = self._start_or_continue_conversation(question)
            conversation_id = conv_data["conversation_id"]
            message_id = conv_data["message_id"]
            
            logger.info(f"Using conversation {conversation_id[:8]} with message {message_id[:8]}")
            
            # Poll for completion
            attempt = 0
            while attempt < self._max_retries:
                status_data = self._get_message_status(conversation_id, message_id)
                status = status_data.get("status")
                
                if status in ["FAILED", "CANCELLED", "QUERY_RESULT_EXPIRED"]:
                    error_msg = f"Query {status.lower()}"
                    logger.error(error_msg)
                    return error_msg
                
                if status == "COMPLETED":
                    try:
                        result_data = self._get_query_result(conversation_id, message_id)
                    except requests.exceptions.RequestException:
                        result_data = None
                    
                    # Check if we have meaningful data in either the response or query results
                    has_meaningful_response = False
                    if "attachments" in status_data:
                        for attachment in status_data["attachments"]:
                            if "text" in attachment and attachment["text"].get("content"):
                                content = attachment["text"]["content"]
                                if content.strip() and content.strip() != question.strip():
                                    has_meaningful_response = True
                                    break
                    
                    has_query_results = (
                        result_data is not None and 
                        "statement_response" in result_data and
                        "result" in result_data["statement_response"] and
                        "data_typed_array" in result_data["statement_response"]["result"] and
                        len(result_data["statement_response"]["result"]["data_typed_array"]) > 0
                    )
                    
                    if has_meaningful_response or has_query_results:
                        return self._extract_response(status_data, result_data)
                
                time.sleep(self._retry_delay)
                attempt += 1
            
            raise TimeoutError(f"Query timed out after {self._max_retries * self._retry_delay} seconds")

        except Exception as e:
            error_msg = f"Error executing Genie request: {str(e)}"
            logger.error(error_msg)
            return error_msg