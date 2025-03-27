from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from typing import List, Optional
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/{job_id}")
async def get_task_statuses(job_id: str, db: Session = Depends(database.get_db)):
    """Get task statuses for a specific job"""
    try:
        # Check if the job exists
        run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get task statuses
        task_statuses = db.query(database.TaskStatus).filter(
            database.TaskStatus.job_id == job_id
        ).order_by(database.TaskStatus.started_at).all()
        
        # Format response
        return {
            "job_id": job_id,
            "status": run.status,
            "tasks": [
                {
                    "id": status.id,
                    "task_id": status.task_id,
                    "status": status.status,
                    "agent_name": status.agent_name,
                    "started_at": status.started_at,
                    "completed_at": status.completed_at
                }
                for status in task_statuses
            ]
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error retrieving task statuses for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 