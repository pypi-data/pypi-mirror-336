import os
import logging
import requests
import base64
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import exists
from ..database import get_async_db, DatabricksConfig

logger = logging.getLogger(__name__)
router = APIRouter()

class DatabricksTokenRequest(BaseModel):
    workspace_url: str = ""  # Default to empty string
    warehouse_id: str = ""  # Make optional with default empty string
    catalog: str = ""  # Make optional with default empty string
    db_schema: str = Field("", alias="schema")  # Make optional with default empty string
    secret_scope: str = ""  # Make optional with default empty string
    enabled: bool = True
    apps_enabled: bool = False

    @property
    def required_fields(self) -> List[str]:
        """Get list of required fields based on configuration"""
        if self.enabled and not self.apps_enabled:
            return ["warehouse_id", "catalog", "schema", "secret_scope"]
        return []

    def validate_required_fields(self) -> None:
        """Validate required fields based on configuration"""
        # Only validate if Databricks is enabled
        if not self.enabled:
            return

        # If apps are enabled, skip validation
        if self.apps_enabled:
            return

        # Check required fields
        empty_fields = []
        for field in self.required_fields:
            # Handle the schema/db_schema field name difference
            if field == "schema":
                value = self.db_schema
            else:
                value = getattr(self, field)
            if not value:
                empty_fields.append(field)
        
        if empty_fields:
            raise ValueError(f"Invalid configuration: {', '.join(empty_fields)} must be non-empty when Databricks is enabled and apps are disabled")

class DatabricksConfigResponse(BaseModel):
    workspace_url: str = ""  # Default to empty string
    warehouse_id: str = ""  # Make optional with default empty string
    catalog: str = ""  # Make optional with default empty string
    db_schema: str = Field("", alias="schema")  # Make optional with default empty string
    secret_scope: str = ""  # Make optional with default empty string
    enabled: bool = True
    apps_enabled: bool = False

async def get_active_config(db: AsyncSession) -> Optional[DatabricksConfig]:
    """Get the currently active Databricks configuration"""
    query = select(DatabricksConfig).where(DatabricksConfig.is_active == True)
    result = await db.execute(query)
    return result.scalar_one_or_none()

@router.post("/config")
async def set_databricks_config(request: DatabricksTokenRequest, db: AsyncSession = Depends(get_async_db)):
    """Set Databricks configuration in the database"""
    try:
        # Validate required fields based on configuration
        request.validate_required_fields()
        
        # Deactivate any existing active configurations
        await db.execute(
            update(DatabricksConfig)
            .where(DatabricksConfig.is_active == True)
            .values(is_active=False)
        )
        
        # If Databricks is disabled, we still create a config but mark it as disabled
        # This allows us to preserve the configuration for when it's re-enabled
        new_config = DatabricksConfig(
            workspace_url=request.workspace_url,
            warehouse_id=request.warehouse_id,
            catalog=request.catalog,
            schema=request.db_schema,  # Use db_schema from request but schema in database
            secret_scope=request.secret_scope,
            is_active=True,
            is_enabled=request.enabled,
            apps_enabled=request.apps_enabled
        )
        
        db.add(new_config)
        await db.commit()
        await db.refresh(new_config)
        
        return {
            "status": "success",
            "message": f"Databricks configuration {'enabled' if request.enabled else 'disabled'} successfully",
            "config": DatabricksConfigResponse(
                workspace_url=new_config.workspace_url,
                warehouse_id=new_config.warehouse_id,
                catalog=new_config.catalog,
                db_schema=new_config.schema,  # Map schema from DB to db_schema in response
                secret_scope=new_config.secret_scope,
                enabled=new_config.is_enabled,
                apps_enabled=new_config.apps_enabled
            )
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error setting Databricks configuration: {str(e)}")

@router.get("/config")
async def get_databricks_config(db: AsyncSession = Depends(get_async_db)):
    """Get current Databricks configuration"""
    config = await get_active_config(db)
    if not config:
        raise HTTPException(status_code=404, detail="Databricks configuration not found")
    
    return DatabricksConfigResponse(
        workspace_url=config.workspace_url,
        warehouse_id=config.warehouse_id,
        catalog=config.catalog,
        db_schema=config.schema,  # Map schema from DB to db_schema in response
        secret_scope=config.secret_scope,
        enabled=config.is_enabled if hasattr(config, 'is_enabled') else True,
        apps_enabled=config.apps_enabled if hasattr(config, 'apps_enabled') else False
    )