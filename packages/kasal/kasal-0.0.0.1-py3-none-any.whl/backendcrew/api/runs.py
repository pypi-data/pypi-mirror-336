from fastapi import FastAPI, HTTPException, WebSocket
from fastapi import APIRouter, Depends
import logging
from sqlalchemy.orm import Session
from .. import database
from typing import List, Optional
from ..api.job_output_streaming import job_output_manager, handle_websocket_connection

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("")
async def list_runs(db: Session = Depends(database.get_db)):
    """Get all runs with their results"""
    try:
        runs = db.query(database.Run).order_by(database.Run.created_at.desc()).all()
        logger.info(f"Retrieved {len(runs)} runs")
        # Convert the SQLAlchemy objects to dictionaries
        return [
            {
                "id": run.id,
                "job_id": run.job_id,
                "status": run.status,
                "inputs": run.inputs,
                "result": run.result,
                "created_at": run.created_at,
                "completed_at": run.completed_at,
                "trigger_type": run.trigger_type,
                "planning": run.planning,
                "run_name": run.run_name
            }
            for run in runs
        ]
    except Exception as e:
        logger.error(f"Error retrieving runs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run_id}")
async def get_run(run_id: int, db: Session = Depends(database.get_db)):
    """Get a specific run by ID"""
    try:
        run = db.query(database.Run).filter(database.Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        return {
            "id": run.id,
            "job_id": run.job_id,
            "status": run.status,
            "inputs": run.inputs,
            "result": run.result,
            "created_at": run.created_at,
            "completed_at": run.completed_at,
            "trigger_type": run.trigger_type,
            "planning": run.planning,
            "run_name": run.run_name
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error retrieving run {run_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.head("/{run_id}")
async def check_run_exists(run_id: int, db: Session = Depends(database.get_db)):
    """Check if a run exists by ID (supports HEAD requests from frontend)"""
    try:
        run = db.query(database.Run).filter(database.Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail=f"Run with ID {run_id} not found")
        return {}  # Return empty response for HEAD request
    except Exception as e:
        logger.error(f"Error checking run existence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run_id}/traces")
async def get_run_traces(run_id: int, db: Session = Depends(database.get_db)):
    """Get traces for a specific run"""
    traces = db.query(database.Trace).filter(database.Trace.run_id == run_id).all()
    if not traces:
        return []
    
    return [
        {
            "id": trace.id,
            "agent_name": trace.agent_name,
            "task_name": trace.task_name,
            "output": trace.output,
            "created_at": trace.created_at
        }
        for trace in traces
    ]

@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for real-time run output streaming."""
    try:
        await handle_websocket_connection(websocket, job_id)
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")
        if websocket.client_state.CONNECTED:
            await websocket.close(code=1000)

@router.get("/{job_id}/outputs")
async def get_run_outputs(
    job_id: str,
    limit: int = 1000,
    offset: int = 0,
    db: Session = Depends(database.get_db)
):
    """Get outputs for a specific run."""
    try:
        # Query job outputs with pagination
        outputs = (
            db.query(database.JobOutput)
            .filter(database.JobOutput.job_id == job_id)
            .order_by(database.JobOutput.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        # Convert to list of dicts
        output_list = [
            {
                "id": output.id,
                "job_id": output.job_id,
                "output": output.output,
                "timestamp": output.timestamp
            }
            for output in outputs
        ]

        return {
            "job_id": job_id,
            "outputs": output_list,
            "limit": limit,
            "offset": offset,
            "total": db.query(database.JobOutput).filter(database.JobOutput.job_id == job_id).count()
        }

    except Exception as e:
        logger.error(f"Error fetching run outputs for {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("")
async def delete_all_runs(db: Session = Depends(database.get_db)):
    """Delete all runs and their associated traces"""
    try:
        logger.info("Attempting to delete all runs and traces")
        # Delete all traces first (due to foreign key constraint)
        trace_count = db.query(database.Trace).delete()
        # Delete all runs
        run_count = db.query(database.Run).delete()
        db.commit()
        logger.info(f"Successfully deleted {run_count} runs and {trace_count} traces")
        return {
            "message": "All runs deleted successfully",
            "deleted_runs": run_count,
            "deleted_traces": trace_count
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting runs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete runs: {str(e)}")

@router.delete("/{run_id}")
async def delete_run(run_id: int, db: Session = Depends(database.get_db)):
    """Delete a specific run and its associated traces"""
    try:
        logger.info(f"Attempting to delete run {run_id} and its traces")
        # Check if the run exists
        run = db.query(database.Run).filter(database.Run.id == run_id).first()
        if not run:
            raise HTTPException(status_code=404, detail=f"Run with ID {run_id} not found")
        
        # Delete associated traces first (due to foreign key constraint)
        trace_count = db.query(database.Trace).filter(database.Trace.run_id == run_id).delete()
        
        # Delete job outputs if they exist
        output_count = db.query(database.JobOutput).filter(database.JobOutput.job_id == run.job_id).delete()
        
        # Delete the run
        db.query(database.Run).filter(database.Run.id == run_id).delete()
        
        db.commit()
        logger.info(f"Successfully deleted run {run_id} with {trace_count} traces and {output_count} outputs")
        
        return {
            "message": f"Run {run_id} deleted successfully",
            "deleted_run_id": run_id,
            "deleted_traces": trace_count,
            "deleted_outputs": output_count
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting run {run_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete run {run_id}: {str(e)}")

@router.get("/{job_id}/debug/outputs")
async def debug_job_outputs(job_id: str, db: Session = Depends(database.get_db)):
    """Debug endpoint to check job outputs in the database."""
    try:
        # Check the run exists
        run = db.query(database.Run).filter(database.Run.job_id == job_id).first()
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
            
        # Get outputs from job_outputs table
        outputs = db.query(database.JobOutput).filter(
            database.JobOutput.job_id == job_id
        ).order_by(database.JobOutput.timestamp).all()
        
        return {
            "run_id": run.id,
            "job_id": job_id,
            "total_outputs": len(outputs),
            "outputs": [
                {
                    "id": output.id,
                    "timestamp": output.timestamp,
                    "task_name": output.task_name,
                    "agent_name": output.agent_name,
                    "output_preview": output.output[:200] if output.output else None
                }
                for output in outputs
            ]
        }
    except Exception as e:
        logger.error(f"Error in debug_job_outputs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

