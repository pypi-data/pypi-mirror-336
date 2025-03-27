"""
Memory management API endpoints.

This module provides FastAPI endpoints for managing memory storage
for CrewAI agents and crews.
"""

import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException

from ..memory_config import MemoryConfig

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("/list", response_model=List[str])
async def list_memories():
    """
    List all crew memories.
    
    Returns:
        List[str]: List of crew names with memory storage
    """
    try:
        memories = MemoryConfig.list_crew_memories()
        return memories
    except Exception as e:
        logger.error(f"Error listing memories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset/{crew_name}", response_model=Dict[str, Any])
async def reset_memory(crew_name: str):
    """
    Reset memory for a specific crew.
    
    Args:
        crew_name: Name of the crew to reset memory for
        
    Returns:
        Dict[str, Any]: Result of the reset operation
    """
    try:
        success = MemoryConfig.reset_crew_memory(crew_name)
        if success:
            return {"status": "success", "message": f"Memory for crew '{crew_name}' has been reset successfully"}
        else:
            return {"status": "error", "message": f"Failed to reset memory for crew '{crew_name}'"}
    except Exception as e:
        logger.error(f"Error resetting memory for crew '{crew_name}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-all", response_model=Dict[str, Any])
async def reset_all_memories():
    """
    Reset all crew memories.
    
    Returns:
        Dict[str, Any]: Result of the reset operation
    """
    try:
        success = MemoryConfig.reset_all_memories()
        if success:
            return {"status": "success", "message": "All crew memories have been reset successfully"}
        else:
            return {"status": "error", "message": "Failed to reset all memories"}
    except Exception as e:
        logger.error(f"Error resetting all memories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 