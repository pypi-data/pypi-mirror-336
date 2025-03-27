from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ValidationError, ConfigDict
import logging
import json
from ..database import get_db, Flow
from datetime import datetime

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

class NodeData(BaseModel):
    label: str
    crewName: Optional[str] = None
    type: Optional[str] = None
    decorator: Optional[str] = None
    listenTo: Optional[List[str]] = None
    routerCondition: Optional[str] = None
    stateType: Optional[str] = None
    stateDefinition: Optional[str] = None
    listener: Optional[Dict[str, Any]] = None

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

class FlowCreate(BaseModel):
    name: str
    crew_id: int
    nodes: List[Node]
    edges: List[Edge]
    flow_config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

class FlowResponse(BaseModel):
    id: int
    name: str
    crew_id: int
    nodes: List[Node]
    edges: List[Edge]
    flow_config: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[FlowResponse])
@router.get("/", response_model=List[FlowResponse], include_in_schema=False)
async def get_all_flows(db: Session = Depends(get_db)):
    flows = db.query(Flow).all()
    return [FlowResponse(
        id=flow.id,
        name=flow.name,
        crew_id=flow.crew_id,
        nodes=flow.nodes or [],
        edges=flow.edges or [],
        flow_config=flow.flow_config or {},
        created_at=flow.created_at.isoformat(),
        updated_at=flow.updated_at.isoformat()
    ) for flow in flows]

@router.get("/{flow_id}", response_model=FlowResponse)
@router.get("/{flow_id}/", response_model=FlowResponse, include_in_schema=False)
async def get_flow(flow_id: int, db: Session = Depends(get_db)):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    return FlowResponse(
        id=flow.id,
        name=flow.name,
        crew_id=flow.crew_id,
        nodes=flow.nodes or [],
        edges=flow.edges or [],
        flow_config=flow.flow_config or {},
        created_at=flow.created_at.isoformat(),
        updated_at=flow.updated_at.isoformat()
    )

@router.post("", response_model=FlowResponse)
@router.post("/", response_model=FlowResponse, include_in_schema=False)
async def create_flow(flow_data: FlowCreate, db: Session = Depends(get_db)):
    try:
        # Debug logging before conversion
        logger.info("Received raw flow data")
        logger.info(f"Name: {flow_data.name}")
        logger.info(f"Crew ID: {flow_data.crew_id}")
        logger.info(f"Number of nodes: {len(flow_data.nodes)}")
        logger.info(f"Number of edges: {len(flow_data.edges)}")
        logger.info(f"Flow config present: {flow_data.flow_config is not None}")
        
        # Log detailed flow config if present
        if flow_data.flow_config:
            logger.info(f"Flow config structure: {type(flow_data.flow_config)}")
            
            # Check for actions specifically
            if 'actions' in flow_data.flow_config:
                actions = flow_data.flow_config['actions']
                logger.info(f"Actions in create flow_config: {type(actions)}, length: {len(actions)}")
                logger.info(f"Actions content: {actions}")
            else:
                logger.warning("No 'actions' key found in flow_config during create")
                # Add empty actions array if missing
                flow_data.flow_config['actions'] = []
                
            # Check for listeners specifically
            if 'listeners' in flow_data.flow_config:
                listeners = flow_data.flow_config['listeners']
                logger.info(f"Listeners in create flow_config: {type(listeners)}, length: {len(listeners)}")
                
                # Check if tasks are included in listeners
                for i, listener in enumerate(listeners):
                    if 'tasks' in listener:
                        tasks = listener['tasks']
                        logger.info(f"Listener {i} tasks during create: {type(tasks)}, length: {len(tasks)}")
        
        # Convert Pydantic model to dict with explicit serialization
        try:
            flow_dict = json.loads(flow_data.json())
            logger.info("Successfully converted flow data to JSON")
            
            # Double check the flow_config and actions are preserved after conversion
            if 'flow_config' in flow_dict:
                if 'actions' in flow_dict['flow_config']:
                    actions = flow_dict['flow_config']['actions']
                    logger.info(f"Actions after conversion: {type(actions)}, length: {len(actions)}")
                else:
                    logger.warning("No 'actions' key in flow_config after conversion")
                    # Ensure actions exists
                    flow_dict['flow_config']['actions'] = []
            else:
                logger.warning("No 'flow_config' in flow_dict after conversion")
        except Exception as e:
            logger.error(f"Error converting flow data to JSON: {str(e)}")
            raise HTTPException(status_code=422, detail=f"Error serializing flow data: {str(e)}")
        
        # Validate the data structure
        try:
            # Check flow_dict for flow_config and actions before creating Flow instance
            flow_config = flow_dict.get('flow_config', {})
            if not 'actions' in flow_config:
                logger.warning("Adding empty actions array to flow_config before creating Flow instance")
                flow_config['actions'] = []
                flow_dict['flow_config'] = flow_config
            
            # Create Flow instance
            flow = Flow(
                name=flow_dict['name'],
                crew_id=flow_dict['crew_id'],
                nodes=flow_dict['nodes'],
                edges=flow_dict['edges'],
                flow_config=flow_dict.get('flow_config', {})
            )
            logger.info("Successfully created Flow instance")
            
            # Verify flow_config and actions in created instance
            if flow.flow_config and 'actions' in flow.flow_config:
                actions = flow.flow_config['actions']
                logger.info(f"Actions in Flow instance: {type(actions)}, length: {len(actions)}")
            else:
                logger.warning("No actions found in Flow instance after creation")
                if not flow.flow_config:
                    flow.flow_config = {}
                flow.flow_config['actions'] = []
                logger.info("Added empty actions array to Flow instance")
        except Exception as e:
            logger.error(f"Error creating Flow instance: {str(e)}")
            logger.error(f"Flow dict: {json.dumps(flow_dict, indent=2)}")
            raise HTTPException(status_code=422, detail=f"Error creating flow: {str(e)}")
        
        try:
            db.add(flow)
            db.commit()
            db.refresh(flow)
            logger.info("Successfully saved flow to database")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # Convert to response format
        try:
            response = FlowResponse(
                id=flow.id,
                name=flow.name,
                crew_id=flow.crew_id,
                nodes=flow.nodes or [],
                edges=flow.edges or [],
                flow_config=flow.flow_config or {},
                created_at=flow.created_at.isoformat(),
                updated_at=flow.updated_at.isoformat()
            )
            logger.info("Successfully created response")
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
async def debug_flow_data(flow_data: FlowCreate):
    """Debug endpoint to validate the data without saving"""
    try:
        # Convert to dict and back to ensure it's valid
        data_dict = flow_data.model_dump()
        logger.info("Data validation successful")
        logger.info(f"Flow name: {data_dict['name']}")
        logger.info(f"Crew ID: {data_dict['crew_id']}")
        logger.info(f"Number of nodes: {len(data_dict['nodes'])}")
        logger.info(f"Number of edges: {len(data_dict['edges'])}")
        logger.info(f"Flow config present: {data_dict.get('flow_config') is not None}")
        
        if data_dict.get('flow_config'):
            logger.info(f"Flow config details: {json.dumps(data_dict['flow_config'], indent=2)}")
        
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

@router.delete("/{flow_id}")
@router.delete("/{flow_id}/", include_in_schema=False)
async def delete_flow(flow_id: int, db: Session = Depends(get_db)):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    try:
        db.delete(flow)
        db.commit()
        return {"status": "success", "message": f"Flow {flow_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting flow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting flow: {str(e)}")

@router.delete("")
@router.delete("/", include_in_schema=False)
async def delete_all_flows(db: Session = Depends(get_db)):
    try:
        db.query(Flow).delete()
        db.commit()
        return {"status": "success", "message": "All flows deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting flows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting flows: {str(e)}")

class FlowUpdate(BaseModel):
    name: str
    flow_config: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)

@router.put("/{flow_id}", response_model=FlowResponse)
@router.put("/{flow_id}/", response_model=FlowResponse, include_in_schema=False)
async def update_flow(flow_id: int, flow_data: FlowUpdate, db: Session = Depends(get_db)):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")
    
    try:
        # Log the incoming flow data for debugging
        logger.info(f"Updating flow {flow_id} with name: {flow_data.name}")
        
        if flow_data.flow_config is not None:
            # Log the structure of flow_config
            logger.info(f"Flow config provided: {type(flow_data.flow_config)}")
            
            # Check for actions specifically
            if 'actions' in flow_data.flow_config:
                actions = flow_data.flow_config['actions']
                logger.info(f"Actions in flow_config: {type(actions)}, length: {len(actions)}")
                logger.info(f"Actions content: {actions}")
            else:
                logger.warning("No 'actions' key found in flow_config")
                # Add empty actions array if missing
                flow_data.flow_config['actions'] = []
                
            # Check for listeners specifically
            if 'listeners' in flow_data.flow_config:
                listeners = flow_data.flow_config['listeners']
                logger.info(f"Listeners in flow_config: {type(listeners)}, length: {len(listeners)}")
                
                # Check if tasks are included in listeners
                for i, listener in enumerate(listeners):
                    if 'tasks' in listener:
                        tasks = listener['tasks']
                        logger.info(f"Listener {i} tasks: {type(tasks)}, length: {len(tasks)}")
                        logger.info(f"Listener {i} tasks content: {tasks}")
        else:
            logger.warning("No flow_config provided in update request")
        
        # Update flow properties
        flow.name = flow_data.name
        if flow_data.flow_config is not None:
            flow.flow_config = flow_data.flow_config
        
        # Update the timestamp
        flow.updated_at = datetime.utcnow()
        
        db.add(flow)
        db.commit()
        db.refresh(flow)
        
        # Log the saved flow_config for verification
        if flow.flow_config:
            logger.info(f"Saved flow_config: {type(flow.flow_config)}")
            
            if 'actions' in flow.flow_config:
                saved_actions = flow.flow_config['actions']
                logger.info(f"Saved actions: {type(saved_actions)}, length: {len(saved_actions)}")
                logger.info(f"Saved actions content: {saved_actions}")
            else:
                logger.warning("No 'actions' key in saved flow_config")
        
        return FlowResponse(
            id=flow.id,
            name=flow.name,
            crew_id=flow.crew_id,
            nodes=flow.nodes or [],
            edges=flow.edges or [],
            flow_config=flow.flow_config or {},
            created_at=flow.created_at.isoformat(),
            updated_at=flow.updated_at.isoformat()
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating flow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error updating flow: {str(e)}") 