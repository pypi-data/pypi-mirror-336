from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db, Agent
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("")
async def create_agent(agent: dict, db: Session = Depends(get_db)):
    """Create a new agent"""
    try:
        # Extract core fields
        db_agent = Agent(
            name=agent.get("name", "Unnamed Agent"),
            role=agent["role"],
            goal=agent["goal"],
            backstory=agent["backstory"],
            
            # Core configuration
            llm=agent.get("llm", "gpt-4"),
            tools=agent.get("tools", []),
            function_calling_llm=agent.get("function_calling_llm"),
            
            # Execution settings
            max_iter=agent.get("max_iter", 25),
            max_rpm=agent.get("max_rpm"),
            max_execution_time=agent.get("max_execution_time"),
            verbose=agent.get("verbose", False),
            allow_delegation=agent.get("allow_delegation", False),
            cache=agent.get("cache", True),
            
            # Memory settings
            memory=agent.get("memory", True),
            embedder_config=agent.get("embedder_config"),
            
            # Templates
            system_template=agent.get("system_template"),
            prompt_template=agent.get("prompt_template"),
            response_template=agent.get("response_template"),
            
            # Code execution settings
            allow_code_execution=agent.get("allow_code_execution", False),
            code_execution_mode=agent.get("code_execution_mode", "safe"),
            
            # Additional settings
            max_retry_limit=agent.get("max_retry_limit", 2),
            use_system_prompt=agent.get("use_system_prompt", True),
            respect_context_window=agent.get("respect_context_window", True),
            
            # Knowledge sources
            knowledge_sources=agent.get("knowledge_sources", []),
        )
        
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_agents(db: Session = Depends(get_db)):
    """Get all agents"""
    try:
        agents = db.query(Agent).all()
        return [
            {
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory,
                "llm": agent.llm,
                "tools": agent.tools,
                "function_calling_llm": agent.function_calling_llm,
                "max_iter": agent.max_iter,
                "max_rpm": agent.max_rpm,
                "max_execution_time": agent.max_execution_time,
                "verbose": agent.verbose,
                "allow_delegation": agent.allow_delegation,
                "cache": agent.cache,
                "memory": agent.memory,
                "embedder_config": agent.embedder_config,
                "system_template": agent.system_template,
                "prompt_template": agent.prompt_template,
                "response_template": agent.response_template,
                "allow_code_execution": agent.allow_code_execution,
                "code_execution_mode": agent.code_execution_mode,
                "max_retry_limit": agent.max_retry_limit,
                "use_system_prompt": agent.use_system_prompt,
                "respect_context_window": agent.respect_context_window,
                "knowledge_sources": agent.knowledge_sources,
                "created_at": agent.created_at
            }
            for agent in agents
        ]
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}")
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get a single agent by ID"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {
            "id": agent.id,
            "name": agent.name,
            "role": agent.role,
            "goal": agent.goal,
            "backstory": agent.backstory,
            "llm": agent.llm,
            "tools": agent.tools,
            "function_calling_llm": agent.function_calling_llm,
            "max_iter": agent.max_iter,
            "max_rpm": agent.max_rpm,
            "max_execution_time": agent.max_execution_time,
            "verbose": agent.verbose,
            "allow_delegation": agent.allow_delegation,
            "cache": agent.cache,
            "memory": agent.memory,
            "embedder_config": agent.embedder_config,
            "system_template": agent.system_template,
            "prompt_template": agent.prompt_template,
            "response_template": agent.response_template,
            "allow_code_execution": agent.allow_code_execution,
            "code_execution_mode": agent.code_execution_mode,
            "max_retry_limit": agent.max_retry_limit,
            "use_system_prompt": agent.use_system_prompt,
            "respect_context_window": agent.respect_context_window,
            "knowledge_sources": agent.knowledge_sources,
            "created_at": agent.created_at
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{agent_id}/full")
async def update_agent_full(agent_id: int, agent: dict, db: Session = Depends(get_db)):
    """Update all fields of an existing agent"""
    try:
        db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not db_agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Update all allowed fields
        updateable_fields = [
            'name', 'role', 'goal', 'backstory', 'llm', 'tools',
            'function_calling_llm', 'max_iter', 'max_rpm', 'max_execution_time',
            'verbose', 'allow_delegation', 'cache', 'memory', 'embedder_config',
            'system_template', 'prompt_template', 'response_template', 'allow_code_execution',
            'code_execution_mode', 'max_retry_limit', 'use_system_prompt',
            'respect_context_window', 'knowledge_sources'
        ]
        
        for field in updateable_fields:
            if field in agent:
                setattr(db_agent, field, agent[field])
        
        db.commit()
        db.refresh(db_agent)
        return db_agent
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{agent_id}")
async def update_agent(agent_id: int, agent: dict, db: Session = Depends(get_db)):
    """Update an existing agent"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Only update specific fields, excluding created_at
    allowed_fields = ['name', 'role', 'goal', 'backstory']
    for field in allowed_fields:
        if field in agent:
            setattr(db_agent, field, agent[field])
    
    try:
        db.commit()
        db.refresh(db_agent)
        return db_agent
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{agent_id}")
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent"""
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        db.delete(db_agent)
        db.commit()
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("")
async def delete_all_agents(db: Session = Depends(get_db)):
    """Delete all agents"""
    try:
        db.query(Agent).delete()
        db.commit()
        return {"message": "All agents deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting all agents: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

