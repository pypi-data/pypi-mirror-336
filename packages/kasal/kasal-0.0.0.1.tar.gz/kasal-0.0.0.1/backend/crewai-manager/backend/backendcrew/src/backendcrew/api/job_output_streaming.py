from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Optional
import logging
import json
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from .. import database
from sqlalchemy.future import select
from ..utils.logger_manager import LoggerManager

# Initialize logger manager
logger_manager = LoggerManager()

class JobOutputManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, job_id: str):
        await websocket.accept()
        async with self._lock:
            if job_id not in self.active_connections:
                self.active_connections[job_id] = set()
            self.active_connections[job_id].add(websocket)
        
        # Send historical messages when client connects
        try:
            async with database.AsyncSessionLocal() as session:
                stmt = select(database.JobOutput).where(
                    database.JobOutput.job_id == job_id
                ).order_by(database.JobOutput.timestamp)
                result = await session.execute(stmt)
                historical_outputs = result.scalars().all()
                
                for output in historical_outputs:
                    await websocket.send_text(json.dumps({
                        "job_id": job_id,
                        "message": output.output,
                        "timestamp": output.timestamp.isoformat(),
                        "type": "historical"
                    }))
        except Exception as e:
            logger_manager.system.error(f"Error sending historical messages: {e}")
        
        logger_manager.system.info(f"Client connected to job {job_id}. Total connections: {len(self.active_connections[job_id])}")

    async def disconnect(self, websocket: WebSocket, job_id: str):
        async with self._lock:
            if job_id in self.active_connections:
                self.active_connections[job_id].discard(websocket)
                if not self.active_connections[job_id]:
                    del self.active_connections[job_id]
        logger_manager.system.info(f"Client disconnected from job {job_id}")

    async def broadcast_to_job(
        self, 
        job_id: str, 
        message: str
    ):
        logger_manager.system.info(f"Starting broadcast for job {job_id}")
        
        # Persist the output to database
        try:
            logger_manager.system.info("Persisting output to database")
            async with database.AsyncSessionLocal() as session:
                job_output = database.JobOutput(
                    job_id=job_id,
                    output=message,
                    timestamp=datetime.utcnow()
                )
                session.add(job_output)
                await session.commit()
                logger_manager.system.info("Successfully persisted output to database")
        except Exception as e:
            logger_manager.system.error(f"Error persisting job output: {e}")
            logger_manager.system.error("Stack trace:", exc_info=True)

        if job_id not in self.active_connections:
            logger_manager.system.info(f"No active connections for job {job_id}")
            return

        message_data = {
            "job_id": job_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "type": "live"
        }

        logger_manager.system.info(f"Broadcasting to {len(self.active_connections[job_id])} connections")
        disconnected = set()
        for connection in self.active_connections[job_id]:
            try:
                await connection.send_text(json.dumps(message_data))
                logger_manager.system.info("Successfully sent message to connection")
            except Exception as e:
                logger_manager.system.error(f"Error sending message to client: {e}")
                logger_manager.system.error("Stack trace:", exc_info=True)
                disconnected.add(connection)

        # Clean up disconnected clients
        if disconnected:
            logger_manager.system.info(f"Cleaning up {len(disconnected)} disconnected clients")
            async with self._lock:
                self.active_connections[job_id] -= disconnected
        
        logger_manager.system.info("Broadcast complete")

    async def get_job_outputs(self, job_id: str, limit: int = 1000, offset: int = 0):
        """Fetch historical job outputs from the database."""
        async with database.AsyncSessionLocal() as session:
            stmt = select(database.JobOutput).where(
                database.JobOutput.job_id == job_id
            ).order_by(
                database.JobOutput.timestamp
            ).offset(offset).limit(limit)
            
            result = await session.execute(stmt)
            outputs = result.scalars().all()
            
            return [
                {
                    "message": output.output,
                    "timestamp": output.timestamp.isoformat()
                }
                for output in outputs
            ]

job_output_manager = JobOutputManager()

async def handle_websocket_connection(websocket: WebSocket, job_id: str):
    try:
        await job_output_manager.connect(websocket, job_id)
        while True:
            # Keep the connection alive
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
    except Exception as e:
        logger_manager.system.error(f"WebSocket error: {e}")
    finally:
        await job_output_manager.disconnect(websocket, job_id) 