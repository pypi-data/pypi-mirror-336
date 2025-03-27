from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db, LLMLog

router = APIRouter()

@router.get("")
async def get_llm_logs(
    page: int = 0,
    per_page: int = 10,
    endpoint: str = None,
    db: Session = Depends(get_db)
):
    """Get LLM API logs with pagination and optional endpoint filtering"""
    query = db.query(LLMLog)
    
    if endpoint and endpoint != 'all':
        query = query.filter(LLMLog.endpoint == endpoint)
    
    # Order by most recent first
    query = query.order_by(LLMLog.created_at.desc())
    
    # Apply pagination
    logs = query.offset(page * per_page).limit(per_page).all()
    
    return logs