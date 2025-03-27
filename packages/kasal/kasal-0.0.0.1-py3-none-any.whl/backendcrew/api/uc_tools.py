from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import logging
from ..uc_client import UCClient
from sqlalchemy.ext.asyncio import AsyncSession
from .databricks import get_active_config
from ..database import get_async_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("")
async def get_uc_tools(db: AsyncSession = Depends(get_async_db)):
    """Get available Unity Catalog tools"""
    try:
        # Get configuration from database
        config = await get_active_config(db)
        if not config:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Databricks configuration not found. Please set the configuration first."
                }
            )

        # Check if Databricks is enabled
        if hasattr(config, 'is_enabled') and not config.is_enabled:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Databricks integration is disabled. Please enable it in the Configuration page."
                }
            )

        # Get token from environment variable - removed check
        token = os.getenv("DATABRICKS_TOKEN", "")  # Default to empty string if not set

        # Map configuration fields
        catalog_name = config.catalog
        schema_name = config.schema
        host = config.workspace_url
        warehouse_id = config.warehouse_id
        
        # Check if workspace_url is provided
        if not host:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Databricks workspace URL is not provided. Please configure it in the Configuration page."
                }
            )

        # Initialize client
        client = UCClient(host=host, token=token)
        
        # List functions
        logger.info(f"Fetching UC tools for catalog: {catalog_name}, schema: {schema_name}")
        functions = client.list_functions(catalog_name=catalog_name, schema_name=schema_name)
        
        # Return empty list if no functions found
        if not functions:
            logger.info("No functions found")
            return []

        # Format the response
        tools = []
        for func in functions:
            try:
                # Get detailed function info
                func_details = client.get_function_details(
                    catalog_name, 
                    schema_name, 
                    func.name
                )
                
                tools.append({
                    "name": func.name,
                    "full_name": f"{catalog_name}.{schema_name}.{func.name}",
                    "catalog": catalog_name,
                    "schema": schema_name,
                    "comment": getattr(func, 'comment', None),
                    "return_type": getattr(func_details, 'return_type', None),
                    "input_params": [
                        {
                            "name": param.name,
                            "type": getattr(param, 'type', {}).get('type_name', 'unknown'),
                            "required": not getattr(param.type, 'nullable', True)
                        }
                        for param in getattr(func_details, 'input_params', []) or []
                    ]
                })
            except Exception as e:
                logger.warning(f"Error processing function {func.name}: {str(e)}")
                continue
        
        logger.info(f"Found {len(tools)} UC tools")
        return tools
        
    except Exception as e:
        logger.error(f"Error getting UC tools: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch Unity Catalog tools: {str(e)}"
        ) 
