import os
import logging
import shutil
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

# Create uploads directory for knowledge files
UPLOADS_DIR = Path(os.environ.get('KNOWLEDGE_DIR', 'uploads/knowledge'))

@router.post("/knowledge")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a knowledge file to be used as a knowledge source"""
    try:
        # Create uploads directory if it doesn't exist
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Generate a safe filename
        file_path = UPLOADS_DIR / file.filename
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Return the file info that can be used in knowledge sources
        return {
            "filename": file.filename,
            "path": str(file.filename),
            "full_path": str(file_path),
            "file_size_bytes": os.path.getsize(file_path),
            "is_uploaded": True,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/knowledge/multi")
async def upload_multiple_knowledge_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload multiple knowledge files in a single request"""
    results = []
    try:
        # Create uploads directory if it doesn't exist
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # Generate a safe filename
            file_path = UPLOADS_DIR / file.filename
            
            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Add file info to results
            results.append({
                "filename": file.filename,
                "path": str(file.filename),
                "full_path": str(file_path),
                "file_size_bytes": os.path.getsize(file_path),
                "is_uploaded": True
            })
        
        return {"files": results, "success": True}
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/check")
async def check_knowledge_file(
    filename: str = Query(..., description="Name of the file to check"),
    db: Session = Depends(get_db)
):
    """Check if a knowledge file exists and get its metadata"""
    try:
        # Check if file exists in uploads directory
        file_path = UPLOADS_DIR / filename
        
        if file_path.exists():
            # Return file metadata
            return {
                "filename": filename,
                "path": str(filename),
                "full_path": str(file_path),
                "file_size_bytes": os.path.getsize(file_path),
                "is_uploaded": True,
                "exists": True
            }
        else:
            return {
                "filename": filename,
                "exists": False,
                "is_uploaded": False
            }
    except Exception as e:
        logger.error(f"Error checking file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/list")
async def list_knowledge_files(
    db: Session = Depends(get_db)
):
    """List all knowledge files in the uploads directory"""
    try:
        # Create uploads directory if it doesn't exist
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        
        files = []
        # List all files in the directory
        for file_path in UPLOADS_DIR.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "path": str(file_path.name),
                    "full_path": str(file_path),
                    "file_size_bytes": os.path.getsize(file_path),
                    "is_uploaded": True
                })
                
        return {"files": files, "success": True}
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 