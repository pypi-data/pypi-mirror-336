from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ValidationError, Field, ConfigDict
import logging
import json
from ..database import get_db, Crew
import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

# Node data models
class Position(BaseModel):
    x: float
    y: float

class Style(BaseModel):
    background: Optional[str] = None
    border: Optional[str] = None
    borderRadius: Optional[str] = None
    padding: Optional[str] = None
    boxShadow: Optional[str] = None

class TaskConfig(BaseModel):
    """Configuration specific to tasks"""
    cache_response: Optional[bool] = False
    cache_ttl: Optional[int] = 3600
    retry_on_fail: Optional[bool] = False
    max_retries: Optional[int] = 3
    timeout: Optional[Any] = None
    priority: Optional[int] = 1
    error_handling: Optional[str] = "default"
    output_file: Optional[str] = None
    output_json: Optional[str] = None
    output_pydantic: Optional[str] = None
    validation_function: Optional[str] = None
    callback_function: Optional[str] = None
    human_input: Optional[bool] = False

class NodeData(BaseModel):
    label: str
    role: Optional[str] = None
    goal: Optional[str] = None
    backstory: Optional[str] = None
    tools: List[Any] = []
    agentId: Optional[int] = None
    taskId: Optional[str] = None
    llm: Optional[str] = None
    function_calling_llm: Optional[str] = None
    max_iter: Optional[int] = None
    max_rpm: Optional[int] = None
    max_execution_time: Optional[int] = None
    verbose: Optional[bool] = None
    allow_delegation: Optional[bool] = None
    cache: Optional[bool] = None
    # Memory settings
    memory: Optional[bool] = True
    embedder_config: Optional[Dict[str, Any]] = None
    system_template: Optional[str] = None
    prompt_template: Optional[str] = None
    response_template: Optional[str] = None
    allow_code_execution: Optional[bool] = None
    code_execution_mode: Optional[str] = None
    max_retry_limit: Optional[int] = None
    use_system_prompt: Optional[bool] = None
    respect_context_window: Optional[bool] = None
    type: Optional[str] = None
    description: Optional[str] = None
    expected_output: Optional[str] = None
    icon: Optional[str] = None
    advanced_config: Optional[Dict[str, Any]] = None
    config: Optional[TaskConfig] = None
    context_tasks: List[str] = []
    async_execution: Optional[bool] = False
    knowledge_sources: Optional[List[Dict[str, Any]]] = None

class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: NodeData
    width: Optional[float] = None
    height: Optional[float] = None
    selected: Optional[bool] = None
    positionAbsolute: Optional[Position] = None
    dragging: Optional[bool] = None
    style: Optional[Style] = None

class Edge(BaseModel):
    source: str
    target: str
    id: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class CrewCreate(BaseModel):
    name: str
    agent_ids: List[int]
    task_ids: List[int]
    nodes: List[Node]
    edges: List[Edge]

    model_config = ConfigDict(from_attributes=True)

class CrewResponse(BaseModel):
    id: int
    name: str
    agent_ids: List[int]
    task_ids: List[int]
    nodes: List[Node]
    edges: List[Edge]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

class CrewStoreResponse(CrewResponse):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    model_config = ConfigDict(from_attributes=True)

class CrewStoreCreateResponse(CrewResponse):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[CrewResponse])
@router.get("/", response_model=List[CrewResponse], include_in_schema=False)
async def get_all_crews(db: Session = Depends(get_db)):
    crews = db.query(Crew).all()
    return [CrewResponse(
        id=crew.id,
        name=crew.name,
        agent_ids=crew.agent_ids,
        task_ids=crew.task_ids,
        nodes=crew.nodes or [],
        edges=crew.edges or [],
        created_at=crew.created_at.isoformat(),
        updated_at=crew.updated_at.isoformat()
    ) for crew in crews]

@router.get("/{crew_id}", response_model=CrewResponse)
@router.get("/{crew_id}/", response_model=CrewResponse, include_in_schema=False)
async def get_crew(crew_id: int, db: Session = Depends(get_db)):
    crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    return CrewResponse(
        id=crew.id,
        name=crew.name,
        agent_ids=crew.agent_ids,
        task_ids=crew.task_ids,
        nodes=crew.nodes or [],
        edges=crew.edges or [],
        created_at=crew.created_at.isoformat(),
        updated_at=crew.updated_at.isoformat()
    )

@router.post("", response_model=CrewResponse)
@router.post("/", response_model=CrewResponse, include_in_schema=False)
async def create_crew(crew_data: CrewCreate, db: Session = Depends(get_db)):
    try:
        # Debug logging before conversion
        logger.info("Received raw crew data")
        logger.info(f"Name: {crew_data.name}")
        logger.info(f"Agent IDs: {crew_data.agent_ids}")
        logger.info(f"Task IDs: {crew_data.task_ids}")
        logger.info(f"Number of nodes: {len(crew_data.nodes)}")
        logger.info(f"Number of edges: {len(crew_data.edges)}")
        
        # Log edge details for debugging
        for i, edge in enumerate(crew_data.edges):
            logger.info(f"Edge {i}: source={edge.source}, target={edge.target}, id={edge.id}")
        
        # Log agent node details including knowledge sources
        for i, node in enumerate(crew_data.nodes):
            if node.type == 'agentNode':
                logger.info(f"Agent node {i}: id={node.id}, label={node.data.label}")
                # Log memory configuration
                memory_status = "enabled" if getattr(node.data, "memory", True) else "disabled"
                logger.info(f"  Memory: {memory_status}")
                if hasattr(node.data, "embedder_config") and node.data.embedder_config:
                    embedder_provider = node.data.embedder_config.get("provider", "openai")
                    embedder_model = node.data.embedder_config.get("config", {}).get("model", "text-embedding-3-small")
                    logger.info(f"  Embedder provider: {embedder_provider}, model: {embedder_model}")
                
                if hasattr(node.data, 'knowledge_sources') and node.data.knowledge_sources:
                    logger.info(f"  Agent {node.id} has {len(node.data.knowledge_sources)} knowledge sources")
                    for j, source in enumerate(node.data.knowledge_sources):
                        logger.info(f"    Knowledge source {j}: {source}")
                else:
                    logger.info(f"  Agent {node.id} has no knowledge sources")
        
        # Convert Pydantic model to dict with explicit serialization
        try:
            crew_dict = json.loads(crew_data.json())
            logger.info("Successfully converted crew data to JSON")
            logger.info(f"JSON edges count: {len(crew_dict.get('edges', []))}")
            
            # Check if knowledge sources were preserved in the JSON
            for node in crew_dict.get('nodes', []):
                if node.get('type') == 'agentNode' and 'data' in node:
                    if 'knowledge_sources' in node['data'] and node['data']['knowledge_sources']:
                        logger.info(f"Node {node['id']} has {len(node['data']['knowledge_sources'])} knowledge sources in JSON")
                    else:
                        logger.info(f"Node {node['id']} has no knowledge sources in JSON")
        except Exception as e:
            logger.error(f"Error converting crew data to JSON: {str(e)}")
            raise HTTPException(status_code=422, detail=f"Error serializing crew data: {str(e)}")
        
        # Validate the data structure
        try:
            # Create crew instance
            crew = Crew(
                name=crew_dict['name'],
                agent_ids=crew_dict['agent_ids'],
                task_ids=crew_dict['task_ids'],
                nodes=crew_dict['nodes'],
                edges=crew_dict['edges']
            )
            logger.info("Successfully created Crew instance")
            logger.info(f"Crew edges count: {len(crew.edges) if crew.edges else 0}")
        except Exception as e:
            logger.error(f"Error creating Crew instance: {str(e)}")
            logger.error(f"Crew dict: {json.dumps(crew_dict, indent=2)}")
            raise HTTPException(status_code=422, detail=f"Error creating crew: {str(e)}")
        
        try:
            db.add(crew)
            db.commit()
            db.refresh(crew)
            logger.info("Successfully saved crew to database")
            logger.info(f"Saved crew edges count: {len(crew.edges) if crew.edges else 0}")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # Convert to response format
        try:
            response = CrewResponse(
                id=crew.id,
                name=crew.name,
                agent_ids=crew.agent_ids,
                task_ids=crew.task_ids,
                nodes=crew.nodes or [],
                edges=crew.edges or [],
                created_at=crew.created_at.isoformat(),
                updated_at=crew.updated_at.isoformat()
            )
            logger.info("Successfully created response")
            logger.info(f"Response edges count: {len(response.edges) if response.edges else 0}")
            return response
        except Exception as e:
            logger.error(f"Error creating response: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating response: {str(e)}")
            
    except ValidationError as e:
        logger.error("Validation error")
        logger.error(e.json())
        raise HTTPException(status_code=422, detail=json.loads(e.json()))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Add a debug endpoint
@router.post("/debug")
async def debug_crew_data(crew_data: CrewCreate):
    """Debug endpoint to validate the data without saving"""
    try:
        # Convert to dict and back to ensure it's valid
        data_dict = crew_data.model_dump()
        logger.info("Data validation successful")
        logger.info(f"Crew name: {data_dict['name']}")
        logger.info(f"Agent IDs: {data_dict['agent_ids']}")
        logger.info(f"Task IDs: {data_dict['task_ids']}")
        logger.info(f"Number of nodes: {len(data_dict['nodes'])}")
        logger.info(f"Number of edges: {len(data_dict['edges'])}")
        return {
            "status": "success",
            "message": "Data validation successful",
            "data": data_dict
        }
    except ValidationError as e:
        logger.error(f"Validation error: {e.json()}")
        return {
            "status": "error",
            "message": "Validation failed",
            "errors": json.loads(e.json())
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }

@router.delete("/{crew_id}")
@router.delete("/{crew_id}/", include_in_schema=False)
async def delete_crew(crew_id: int, db: Session = Depends(get_db)):
    """Delete a crew by ID"""
    crew = db.query(Crew).filter(Crew.id == crew_id).first()
    if not crew:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    db.delete(crew)
    db.commit()
    return {"detail": "Crew deleted successfully"}

@router.delete("")
@router.delete("/", include_in_schema=False)
async def delete_all_crews(db: Session = Depends(get_db)):
    """Delete all crews"""
    db.query(Crew).delete()
    db.commit()
    return {"detail": "All crews deleted successfully"} 