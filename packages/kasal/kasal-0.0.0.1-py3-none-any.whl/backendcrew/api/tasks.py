from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db, Task
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
import datetime
import json

class ConditionConfig(BaseModel):
    type: str
    parameters: Dict[str, Any]
    dependent_task: Optional[str] = None

class TaskConfig(BaseModel):
    cache_response: Optional[bool] = None
    cache_ttl: Optional[int] = None
    retry_on_fail: Optional[bool] = None
    max_retries: Optional[int] = None
    timeout: Optional[int] = None
    priority: Optional[int] = None
    error_handling: Optional[str] = None
    output_file: Optional[str] = None
    output_json: Optional[str] = None
    output_pydantic: Optional[str] = None
    callback: Optional[str] = None
    human_input: Optional[bool] = None
    condition: Optional[ConditionConfig] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    agent_id: int
    expected_output: str
    tools: List[str]
    async_execution: bool
    context: List[int]
    config: TaskConfig
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("")
async def create_task(task: dict, db: Session = Depends(get_db)):
    """Create a new task"""
    try:
        # Extract config values with defaults
        config = task.get("config", {})
        
        # Handle condition if present
        if "condition" in task:
            if config is None:
                config = {}
            config["condition"] = {
                "type": task["condition"].get("type"),
                "parameters": task["condition"].get("parameters", {}),
                "dependent_task": task["condition"].get("dependent_task")
            }
        
        # Handle callback field
        callback = None
        if "callback" in task:
            callback = task["callback"]
        elif config and "callback" in config:
            callback = config["callback"]
        
        # Set advanced configuration fields from config if present
        db_task = Task(
            name=task["name"],
            description=task["description"],
            agent_id=task.get("agent_id"),
            expected_output=task["expected_output"],
            tools=task.get("tools", []),
            async_execution=task.get("async_execution", False),
            context=task.get("context", []),
            config=config,
            output_json=config.get("output_json") if "output_json" in config else task.get("output_json"),
            output_pydantic=config.get("output_pydantic") if "output_pydantic" in config else task.get("output_pydantic"),
            output_file=config.get("output_file") if "output_file" in config else task.get("output_file"),
            output=task.get("output"),
            callback=callback,
            human_input=config.get("human_input") if "human_input" in config else task.get("human_input", False),
            converter_cls=task.get("converter_cls")
        )
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_tasks(db: Session = Depends(get_db)):
    """Get all tasks"""
    try:
        tasks = db.query(Task).all()
        return [
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "agent_id": task.agent_id,
                "expected_output": task.expected_output,
                "tools": task.tools,
                "async_execution": task.async_execution,
                "context": task.context,
                "config": task.config,
                "output_json": task.output_json,
                "output_pydantic": task.output_pydantic,
                "output_file": task.output_file,
                "output": task.output,
                "callback": task.callback,
                "human_input": task.human_input,
                "converter_cls": task.converter_cls,
                "created_at": task.created_at,
                "updated_at": task.updated_at
            }
            for task in tasks
        ]
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}")
async def update_task(task_id: int, task: dict, db: Session = Depends(get_db)):
    """Update an existing task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        # Handle condition update if present
        if "condition" in task:
            if db_task.config is None:
                db_task.config = {}
            db_task.config["condition"] = {
                "type": task["condition"].get("type"),
                "parameters": task["condition"].get("parameters", {}),
                "dependent_task": task["condition"].get("dependent_task")
            }
        elif task.get("config", {}).get("condition") is None and db_task.config:
            # Remove condition if it's explicitly set to None
            if "condition" in db_task.config:
                del db_task.config["condition"]
        
        # Handle callback field
        if "callback" in task:
            db_task.callback = task["callback"]
        elif task.get("config", {}).get("callback") is not None:
            db_task.callback = task["config"]["callback"]
        
        # Update other fields
        db_task.name = task.get("name", db_task.name)
        db_task.description = task.get("description", db_task.description)
        db_task.agent_id = task.get("agent_id", db_task.agent_id)
        db_task.expected_output = task.get("expected_output", db_task.expected_output)
        db_task.tools = task.get("tools", db_task.tools)
        db_task.async_execution = task.get("async_execution", db_task.async_execution)
        db_task.context = task.get("context", db_task.context)
        
        # Update config while preserving condition if it exists
        if "config" in task:
            new_config = task["config"]
            if db_task.config and "condition" in db_task.config and "condition" not in new_config:
                new_config["condition"] = db_task.config["condition"]
            db_task.config = new_config
        
        db_task.output_json = task.get("output_json", db_task.output_json)
        db_task.output_pydantic = task.get("output_pydantic", db_task.output_pydantic)
        db_task.output_file = task.get("output_file", db_task.output_file)
        db_task.output = task.get("output", db_task.output)
        db_task.human_input = task.get("human_input", db_task.human_input)
        db_task.converter_cls = task.get("converter_cls", db_task.converter_cls)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        db.delete(db_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("")
async def delete_all_tasks(db: Session = Depends(get_db)):
    """Delete all tasks"""
    try:
        db.query(Task).delete()
        db.commit()
        return {"message": "All tasks deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting all tasks: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        logger.error(f"Error getting task: {str(e)}")
        raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}/full")
async def update_task_full(task_id: int, task: dict, db: Session = Depends(get_db)):
    """Update all fields of an existing task"""
    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update all fields
        updateable_fields = [
            'name', 'description', 'agent_id', 'expected_output',
            'tools', 'async_execution', 'context', 'config',
            'output_json', 'output_pydantic', 'output_file',
            'output', 'callback', 'human_input', 'converter_cls'
        ]
        
        for field in updateable_fields:
            if field in task:
                setattr(db_task, field, task[field])
        
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

