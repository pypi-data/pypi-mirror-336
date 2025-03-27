from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Run(Base):
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    # ... other fields

class Trace(Base):
    __tablename__ = "traces"
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    agent_name = Column(String)
    task_name = Column(String)
    output = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    # ... other fields 