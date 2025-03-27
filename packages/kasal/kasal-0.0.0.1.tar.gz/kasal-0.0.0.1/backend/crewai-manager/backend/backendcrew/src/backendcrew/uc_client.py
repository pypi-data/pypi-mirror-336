import os
import logging
from databricks.sdk import WorkspaceClient
from typing import List, Optional

logger = logging.getLogger(__name__)

class MockFunction:
    def __init__(self, name: str, comment: str = None):
        self.name = name
        self.comment = comment
        self.return_type = "string"
        self.input_params = []

class UCClient:
    def __init__(self, host: Optional[str] = None, token: Optional[str] = None, mock_mode: bool = False):
        self.mock_mode = mock_mode or os.getenv("UC_MOCK_MODE", "").lower() == "true"
        if not self.mock_mode:
            self.client = self.initialize_uc_client(host, token)

    def initialize_uc_client(self, host: Optional[str] = None, token: Optional[str] = None):
        """Initialize Unity Catalog client and set it as global client"""
        try:
            # Use provided host and token, fall back to environment variables if not provided
            host = host or os.getenv("DATABRICKS_HOST")
            token = token or os.getenv("DATABRICKS_TOKEN")

            if not host or not token:
                raise ValueError("Host and token must be provided either as parameters or through environment variables")

            logger.info(f"Initializing Databricks client with host: {host}")
            client = WorkspaceClient(host=host, token=token)
            logger.info("Successfully initialized Databricks client")
            return client
        except Exception as e:
            logger.error(f"Error initializing UC client: {str(e)}")
            raise

    def list_functions(self, catalog_name: str, schema_name: str) -> List[MockFunction]:
        """List functions in a specific catalog and schema"""
        if self.mock_mode:
            # Return mock data for development
            return [
                MockFunction("example_function_1", "This is an example function"),
                MockFunction("example_function_2", "Another example function"),
            ]

        try:
            logger.info(f"Listing functions in {catalog_name}.{schema_name}")
            functions = self.client.functions.list(
                catalog_name=catalog_name,
                schema_name=schema_name
            )
            functions_list = list(functions)
            logger.info(f"Found {len(functions_list)} functions")
            return functions_list
        except Exception as e:
            logger.error(f"Error listing functions: {str(e)}")
            raise

    def get_function_details(self, catalog_name: str, schema_name: str, function_name: str) -> Optional[MockFunction]:
        """Get details of a specific function"""
        if self.mock_mode:
            # Return mock data for the specified function
            mock_functions = {
                "example_function_1": MockFunction("example_function_1", "This is an example function"),
                "example_function_2": MockFunction("example_function_2", "Another example function"),
            }
            if function_name in mock_functions:
                return mock_functions[function_name]
            raise ValueError(f"Function {function_name} not found")

        try:
            functions = self.list_functions(catalog_name, schema_name)
            for func in functions:
                if func.name == function_name:
                    return func
            raise ValueError(f"Function {function_name} not found")
        except Exception as e:
            logger.error(f"Error getting function details: {str(e)}")
            raise
