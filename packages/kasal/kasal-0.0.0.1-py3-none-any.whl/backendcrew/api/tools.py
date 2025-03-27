from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db, Tool
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("")
async def create_tool(tool: dict, db: Session = Depends(get_db)):
    """Create a new tool"""
    try:
        db_tool = Tool(
            title=tool["title"],
            description=tool["description"],
            icon=tool["icon"],
            config=tool.get("config", {})
        )
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_tools(db: Session = Depends(get_db)):
    """Get all tools"""
    try:
        tools = db.query(Tool).all()
        logger.info(f"Retrieved {len(tools)} tools from database")
        return tools
    except Exception as e:
        logger.error(f"Error retrieving tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tool_id}")
async def get_tool(tool_id: int, db: Session = Depends(get_db)):
    """Get a single tool by ID"""
    try:
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        logger.info(f"Retrieved tool {tool_id} from database")
        return tool
    except Exception as e:
        logger.error(f"Error retrieving tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{tool_id}")
async def update_tool(tool_id: int, tool: dict, db: Session = Depends(get_db)):
    """Update an existing tool"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    try:
        if "config" in tool:
            current_config = db_tool.config or {}
            logger.info(f"Current config for tool {tool_id}: {current_config}")
            logger.info(f"New config values being added: {tool['config']}")
            
            # If tool['config'] is empty, clear the config
            if not tool['config']:
                db_tool.config = {}
                logger.info("Clearing config as empty update was received")
            else:
                # Create a new dictionary for the update
                new_config = dict(current_config)
                new_config.update(tool['config'])
                logger.info(f"Updated config for tool {tool_id}: {new_config}")
                
                # Set the new config directly
                db_tool.config = new_config
            
            logger.info(f"Config right after setting: {db_tool.config}")
        
        # Update other fields
        for key, value in tool.items():
            if key != "config":
                setattr(db_tool, key, value)
        
        logger.info(f"Config before commit: {db_tool.config}")
        db.commit()
        logger.info(f"Config after commit before refresh: {db_tool.config}")
        db.refresh(db_tool)
        logger.info(f"Config after refresh: {db_tool.config}")
        
        # Verify the update
        persisted_tool = db.query(Tool).filter(Tool.id == tool_id).first()
        logger.info(f"Config after fresh query: {persisted_tool.config}")
        return db_tool
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{tool_id}")
async def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    """Delete a tool"""
    db_tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not db_tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    try:
        db.delete(db_tool)
        db.commit()
        return {"message": "Tool deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

