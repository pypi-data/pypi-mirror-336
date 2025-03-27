from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, UTC
import os
import logging
import aiosqlite
from typing import Dict
from pathlib import Path

Base = declarative_base()

logger = logging.getLogger(__name__)

# Define database path
package_dir = Path(__file__).resolve().parent
DB_PATH = str(package_dir / 'crewai.db')

# Ensure directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

class DatabricksConfig(Base):
    __tablename__ = "databricks_configs"
    
    id = Column(Integer, primary_key=True)
    workspace_url = Column(String, nullable=True, default="")  # Make nullable with empty string default
    warehouse_id = Column(String, nullable=False)
    catalog = Column(String, nullable=False)
    schema = Column(String, nullable=False)
    secret_scope = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # To track the currently active configuration
    is_enabled = Column(Boolean, default=True)  # To enable/disable Databricks integration
    apps_enabled = Column(Boolean, default=False)  # To enable/disable Databricks apps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    backstory = Column(String)
    
    # Core configuration
    llm = Column(String, default="gpt-4")
    tools = Column(JSON, default=list, nullable=False)
    function_calling_llm = Column(String)
    
    # Execution settings
    max_iter = Column(Integer, default=25)
    max_rpm = Column(Integer)
    max_execution_time = Column(Integer)
    verbose = Column(Boolean, default=False)
    allow_delegation = Column(Boolean, default=False)
    cache = Column(Boolean, default=True)
    
    # Memory settings
    memory = Column(Boolean, default=True)
    embedder_config = Column(JSON)
    
    # Templates
    system_template = Column(String)
    prompt_template = Column(String)
    response_template = Column(String)
    
    # Code execution settings
    allow_code_execution = Column(Boolean, default=False)
    code_execution_mode = Column(String, default='safe')
    
    # Additional settings
    max_retry_limit = Column(Integer, default=2)
    use_system_prompt = Column(Boolean, default=True)
    respect_context_window = Column(Boolean, default=True)
    
    # Knowledge sources
    knowledge_sources = Column(JSON, default=list)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Agent, self).__init__(**kwargs)
        if self.tools is None:
            self.tools = []

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)
    expected_output = Column(String, nullable=False)
    tools = Column(JSON, default=list)
    async_execution = Column(Boolean, default=False)
    context = Column(JSON, default=list)  # Store list of related task IDs
    config = Column(JSON)  # For additional configuration including conditions
    output_json = Column(JSON)
    output_pydantic = Column(JSON)
    output_file = Column(String)
    output = Column(JSON)  # For storing task output
    callback = Column(String)  # Store callback function name/reference
    human_input = Column(Boolean, default=False)
    converter_cls = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    agent = relationship("Agent")
    
    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        if self.tools is None:
            self.tools = []
        if self.context is None:
            self.context = []
        if self.config is None:
            self.config = {}
        # Ensure condition is properly structured in config if present
        if 'condition' in kwargs:
            if self.config is None:
                self.config = {}
            self.config['condition'] = {
                'type': kwargs['condition'].get('type'),
                'parameters': kwargs['condition'].get('parameters', {}),
                'dependent_task': kwargs['condition'].get('dependent_task')
            }

class Run(Base):
    __tablename__ = "runs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    status = Column(String)
    inputs = Column(JSON)
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    planning = Column(Boolean, default=False)
    trigger_type = Column(String, default="manual")
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    run_name = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    outputs = relationship("JobOutput", back_populates="run", order_by="JobOutput.timestamp")

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    config = Column(JSON)  # For tool-specific configurations
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        if 'config' not in kwargs:
            kwargs['config'] = {}
        super(Tool, self).__init__(**kwargs)

class LLMLog(Base):
    __tablename__ = "llm_logs"
    
    id = Column(Integer, primary_key=True)
    endpoint = Column(String, nullable=False)  # e.g., 'generate-crew', 'generate-agent'
    prompt = Column(String, nullable=False)    # The input prompt
    response = Column(String, nullable=False)   # The LLM response
    model = Column(String, nullable=False)     # e.g., 'gpt-4'
    tokens_used = Column(Integer)              # Total tokens used
    duration_ms = Column(Integer)              # Time taken in milliseconds
    status = Column(String, nullable=False)    # 'success' or 'error'
    error_message = Column(String)             # Error message if any
    created_at = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(JSON)                  # Any additional metadata (renamed from metadata)

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(String, primary_key=True)  # e.g., 'job-posting'
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    agents = Column(JSON, nullable=False)  # List of agent IDs
    difficulty = Column(String, nullable=False)
    agents_yaml = Column(String)  # Store the agents.yaml content
    tasks_yaml = Column(String)   # Store the tasks.yaml content
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Trace(Base):
    __tablename__ = "traces"
    
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('runs.id'))
    agent_name = Column(String, nullable=False)
    task_name = Column(String, nullable=False)
    output = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with Run
    run = relationship("Run", backref="traces")

class Crew(Base):
    __tablename__ = "crews"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    agent_ids = Column(JSON, default=list, nullable=False)
    task_ids = Column(JSON, default=list, nullable=False)
    nodes = Column(JSON, default=list, nullable=False)
    edges = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Crew, self).__init__(**kwargs)
        if self.agent_ids is None:
            self.agent_ids = []
        if self.task_ids is None:
            self.task_ids = []
        if self.nodes is None:
            self.nodes = []
        if self.edges is None:
            self.edges = []

# Keeping Plan class for backward compatibility, but making it use the same table
class Plan(Crew):
    pass

class Flow(Base):
    __tablename__ = "flows"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    crew_id = Column(Integer, nullable=False)
    nodes = Column(JSON, default=list, nullable=False)
    edges = Column(JSON, default=list, nullable=False)
    flow_config = Column(JSON, default=dict, nullable=True)  # Store listeners, actions, starting points
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Flow, self).__init__(**kwargs)
        if self.nodes is None:
            self.nodes = []
        if self.edges is None:
            self.edges = []
        if self.flow_config is None:
            self.flow_config = {}

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cron_expression = Column(String, nullable=False)  # Cron expression for schedule timing
    agents_yaml = Column(JSON, nullable=False)  # Store agents configuration
    tasks_yaml = Column(JSON, nullable=False)  # Store tasks configuration
    inputs = Column(JSON, default=dict)  # Additional inputs for the job
    is_active = Column(Boolean, default=True)  # Whether the schedule is active
    planning = Column(Boolean, default=False)  # Whether planning is enabled
    model = Column(String, default="gpt-4o-mini")  # Model to use for planning
    last_run_at = Column(DateTime, nullable=True)  # Last time the schedule was executed
    next_run_at = Column(DateTime, nullable=True)  # Next scheduled run time
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobOutput(Base):
    __tablename__ = "job_outputs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("runs.job_id"), index=True)
    output = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=datetime.now(UTC))

    # Relationship to the run
    run = relationship("Run", back_populates="outputs")

class TaskStatus(Base):
    __tablename__ = "task_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("runs.job_id"), index=True)
    task_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)  # 'running', 'completed', or 'failed'
    agent_name = Column(String, nullable=True)  # Store the name of the agent handling this task
    started_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship to the run
    run = relationship("Run", backref="task_statuses")

class ErrorTrace(Base):
    __tablename__ = "error_traces"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), index=True)
    task_key = Column(String, nullable=False, index=True)
    error_type = Column(String, nullable=False)
    error_message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.now(UTC))
    error_metadata = Column(JSON, default=dict)
    
    # Relationship to the run
    run = relationship("Run", backref="error_traces")

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    encrypted_value = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))

# Create async SQLite engine
logger.info(f"Using database at: {DB_PATH}")
async_engine = create_async_engine(f'sqlite+aiosqlite:///{DB_PATH}')
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create tables if they don't exist
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized")

# Async database dependency
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Keep the sync version for backward compatibility if needed
engine = create_engine(f'sqlite:///{DB_PATH}')
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
