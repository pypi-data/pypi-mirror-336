"""
Utilities for tracking task statuses across job execution.
"""
from datetime import datetime, UTC
from typing import Dict, Any, Optional, List, Callable
from sqlalchemy.orm import Session

from .. import database
from ..utils.logger_manager import LoggerManager

# Initialize logger manager
logger_manager = LoggerManager()

class TaskStatus:
    """Task status constants"""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

def create_task_status(db: Session, job_id: str, task_id: str, agent_name: Optional[str] = None) -> database.TaskStatus:
    """
    Create a new task status entry with RUNNING status.
    
    Args:
        db: Database session
        job_id: The ID of the job
        task_id: The ID/key of the task
        agent_name: The name of the agent assigned to this task (optional)
        
    Returns:
        database.TaskStatus: The created task status record
    """
    logger_manager.crew.info(f"Creating task status for job {job_id}, task {task_id}, agent {agent_name}")
    
    # Check if status already exists
    existing = db.query(database.TaskStatus).filter(
        database.TaskStatus.job_id == job_id,
        database.TaskStatus.task_id == task_id
    ).first()
    
    if existing:
        logger_manager.crew.info(f"Task status already exists for job {job_id}, task {task_id}")
        return existing
    
    # Create new status entry
    task_status = database.TaskStatus(
        job_id=job_id,
        task_id=task_id,
        status=TaskStatus.RUNNING,
        agent_name=agent_name,
        started_at=datetime.now(UTC),
        completed_at=None
    )
    
    # Add to database
    db.add(task_status)
    db.commit()
    db.refresh(task_status)
    
    logger_manager.crew.info(f"Created task status record: {task_status.id}")
    return task_status

def update_task_status(db: Session, job_id: str, task_id: str, status: str) -> database.TaskStatus:
    """
    Update the status of a task.
    
    Args:
        db: Database session
        job_id: The ID of the job
        task_id: The ID/key of the task
        status: The new status (use TaskStatus constants)
        
    Returns:
        database.TaskStatus: The updated task status record
    """
    logger_manager.crew.info(f"Updating task status for job {job_id}, task {task_id} to {status}")
    
    # Get existing task status
    task_status = db.query(database.TaskStatus).filter(
        database.TaskStatus.job_id == job_id,
        database.TaskStatus.task_id == task_id
    ).first()
    
    if not task_status:
        logger_manager.crew.warning(f"No task status found for job {job_id}, task {task_id}")
        return None
    
    # Update status
    task_status.status = status
    
    # If status is completed or failed, update completed_at
    if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
        task_status.completed_at = datetime.now(UTC)
    
    # Commit changes
    db.commit()
    db.refresh(task_status)
    
    logger_manager.crew.info(f"Updated task status to {status} for job {job_id}, task {task_id}")
    return task_status

def get_task_status(db: Session, job_id: str, task_id: str) -> database.TaskStatus:
    """
    Get the current status of a task.
    
    Args:
        db: Database session
        job_id: The ID of the job
        task_id: The ID/key of the task
        
    Returns:
        database.TaskStatus: The task status record or None if not found
    """
    return db.query(database.TaskStatus).filter(
        database.TaskStatus.job_id == job_id,
        database.TaskStatus.task_id == task_id
    ).first()

def get_all_task_statuses(db: Session, job_id: str) -> List[database.TaskStatus]:
    """
    Get all task statuses for a job.
    
    Args:
        db: Database session
        job_id: The ID of the job
        
    Returns:
        List[database.TaskStatus]: List of task status records
    """
    return db.query(database.TaskStatus).filter(
        database.TaskStatus.job_id == job_id
    ).order_by(database.TaskStatus.started_at).all()

def create_task_statuses_for_job(db: Session, job_id: str, tasks_yaml: Dict[str, Dict]) -> List[database.TaskStatus]:
    """
    Create task status entries for all tasks in a job with RUNNING status.
    
    Args:
        db: Database session
        job_id: The ID of the job
        tasks_yaml: Dictionary of tasks with their configurations
        
    Returns:
        List[database.TaskStatus]: List of created task status records
    """
    logger_manager.crew.info(f"Creating task statuses for all tasks in job {job_id}")
    
    created_statuses = []
    
    for task_key, task_config in tasks_yaml.items():
        # Get the agent assigned to this task
        agent_name = task_config.get('agent')
        
        # Create task status entry
        task_status = create_task_status(db, job_id, task_key, agent_name)
        created_statuses.append(task_status)
    
    logger_manager.crew.info(f"Created {len(created_statuses)} task status records for job {job_id}")
    return created_statuses

def create_task_callbacks(db: Session, job_id: str, task_id: str) -> Dict[str, Callable]:
    """
    Create a set of callback functions for updating task status.
    
    Args:
        db: Database session
        job_id: The ID of the job
        task_id: The ID/key of the task
        
    Returns:
        Dict containing 'on_start', 'on_end', and 'on_error' functions
    """
    def on_start():
        """Update task status to RUNNING when it starts"""
        try:
            logger_manager.crew.info(f"Task {task_id} in job {job_id} is starting")
            update_task_status(db, job_id, task_id, TaskStatus.RUNNING)
        except Exception as e:
            logger_manager.crew.error(f"Error updating task status to RUNNING: {str(e)}")
    
    def on_end(output):
        """Update task status to COMPLETED when it finishes"""
        try:
            logger_manager.crew.info(f"Task {task_id} in job {job_id} completed with output: {output}")
            update_task_status(db, job_id, task_id, TaskStatus.COMPLETED)
            return output
        except Exception as e:
            logger_manager.crew.error(f"Error updating task status to COMPLETED: {str(e)}")
            return output
    
    def on_error(error):
        """Update task status to FAILED when it encounters an error"""
        try:
            logger_manager.crew.error(f"Task {task_id} in job {job_id} failed: {str(error)}")
            update_task_status(db, job_id, task_id, TaskStatus.FAILED)
        except Exception as e:
            logger_manager.crew.error(f"Error updating task status to FAILED: {str(e)}")
    
    return {
        "on_start": on_start,
        "on_end": on_end,
        "on_error": on_error
    } 