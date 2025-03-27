"""
Implementation for CrewAI Flow execution.
"""
import logging
import os
from typing import Dict, Type, List, Optional, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from crewai import Agent, Task, Crew
from crewai import Process
from crewai.flow.flow import Flow as CrewAIFlow
from crewai.flow.flow import start, listen, and_, or_

from .utils.logger_manager import LoggerManager
from .utils.crew_helpers import create_agent, create_task, is_data_missing
from .llm_config import LLMConfig, ModelProvider
from .tools.tool_factory import ToolFactory
from .database import SessionLocal, Run, Flow as FlowModel

# Initialize logger manager
logger_manager = LoggerManager()

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Backendflow:
    """Base Backendflow class for handling flow execution"""

    def __init__(self, job_id: Optional[str] = None, flow_id: Optional[int] = None):
        """
        Initialize a new Backendflow instance.
        
        Args:
            job_id: Optional job ID for tracking
            flow_id: Optional flow ID to load from database
        """
        self._job_id = job_id
        self._flow_id = flow_id
        self._flow_data = None
        self._output_dir = None
        self._config = {
            'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY'),
            'openai_api_key': LLMConfig.get_api_key(),
            'serper_api_key': os.getenv('SERPER_API_KEY'),
        }
        logger.info(f"Initializing Backendflow{' for job ' + job_id if job_id else ''}")

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    @property
    def output_dir(self):
        logger.info(f"Getting output_dir: {self._output_dir}")
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value):
        logger.info(f"Setting output_dir to: {value}")
        if value is not None:
            os.makedirs(value, exist_ok=True)
        self._output_dir = value

    def load_flow(self) -> Dict:
        """Load flow data from the database"""
        logger.info(f"Loading flow with ID: {self._flow_id}")
        
        if not self._flow_id:
            logger.error("No flow_id provided")
            raise ValueError("No flow_id provided")
            
        db = SessionLocal()
        try:
            flow = db.query(FlowModel).filter(FlowModel.id == self._flow_id).first()
            if not flow:
                logger.error(f"Flow with ID {self._flow_id} not found")
                raise ValueError(f"Flow with ID {self._flow_id} not found")
                
            self._flow_data = {
                'id': flow.id,
                'name': flow.name,
                'crew_id': flow.crew_id,
                'nodes': flow.nodes,
                'edges': flow.edges,
                'flow_config': flow.flow_config
            }
            logger.info(f"Successfully loaded flow: {flow.name}")
            return self._flow_data
        finally:
            db.close()

    def flow(self) -> CrewAIFlow:
        """Creates and returns a CrewAI Flow instance based on the loaded flow configuration"""
        logger.info("Creating CrewAI Flow")
        
        if not self._flow_data:
            self.load_flow()
            
        if not self._flow_data:
            logger.error("Flow data could not be loaded")
            raise ValueError("Flow data could not be loaded")
        
        try:
            # Configure flow based on flow_config
            flow_config = self._flow_data.get('flow_config', {})
            
            if not flow_config:
                logger.warning("No flow_config found in flow data")
                # Try to parse flow_config from a string if needed
                if isinstance(self._flow_data.get('flow_config'), str):
                    try:
                        import json
                        flow_config = json.loads(self._flow_data.get('flow_config'))
                        logger.info("Successfully parsed flow_config from string")
                    except Exception as e:
                        logger.error(f"Failed to parse flow_config string: {e}")
            
            # Check for starting points
            starting_points = flow_config.get('startingPoints', [])
            if not starting_points:
                logger.error("No starting points defined in flow configuration")
                raise ValueError("No starting points defined in flow configuration")
            
            logger.info(f"Found {len(starting_points)} starting points in flow config")
            
            # For simplicity, use the first starting point
            start_point = starting_points[0]
            crew_name = start_point.get('crewName')
            crew_id = start_point.get('crewId')
            task_name = start_point.get('taskName')
            task_id = start_point.get('taskId')
            
            logger.info(f"Configuring start point: Crew={crew_name}({crew_id}), Task={task_name}({task_id})")
            
            # Open database connection to fetch actual agent and task data
            db = SessionLocal()
            try:
                # Import necessary database models
                from .database import Agent as AgentModel
                from .database import Task as TaskModel
                from .database import Tool as ToolModel
                from .callbacks import JobOutputCallback
                
                # Create streaming callback for job output if we have a job_id
                streaming_cb = None
                if self._job_id:
                    streaming_cb = JobOutputCallback(job_id=self._job_id, max_retries=3)
                    logger.info(f"Created streaming callback for job {self._job_id}")
                
                # Query the database for the task information first
                task_data = db.query(TaskModel).filter(TaskModel.id == task_id).first()
                
                if not task_data:
                    logger.warning(f"Task with ID {task_id} not found, creating a default task")
                    # We'll create a default task after agent creation
                    task_description = f"Execute {task_name} task from {crew_name} crew"
                    task_expected_output = "Flow task executed successfully"
                    agent_id = None
                else:
                    # Get the agent_id from the task data instead of hardcoding
                    agent_id = task_data.agent_id
                    logger.info(f"Found task data: {task_data.name}, {task_data.description}")
                    if agent_id is None:
                        logger.warning(f"Task {task_id} does not have an associated agent_id")
                
                # Query the database for the agent information
                if agent_id is not None:
                    agent_data = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
                else:
                    agent_data = None
                
                if not agent_data:
                    logger.warning(f"Agent with ID {agent_id} not found, creating a default agent")
                    # Create a default agent with appropriate configuration
                    agent = Agent(
                        role=f"Agent for {task_name}",
                        goal=f"Execute the {task_name} task from the {crew_name} crew",
                        backstory=f"I am responsible for starting the flow with {task_name}",
                        allow_delegation=False,
                        verbose=True
                    )
                else:
                    # Create agent from database data
                    logger.info(f"Found agent data: {agent_data.name}, {agent_data.role}")
                    
                    # Get tools for the agent
                    tools = []
                    tool_factory = ToolFactory(self._config)
                    
                    if agent_data.tools:
                        for tool_id in agent_data.tools:
                            tool_record = db.query(ToolModel).filter(ToolModel.id == tool_id).first()
                            if tool_record:
                                tool_name = tool_record.title
                                tool = tool_factory.create_tool(tool_name)
                                if tool:
                                    tools.append(tool)
                                    logger.info(f"Added tool: {tool_name} to agent: {agent_data.name}")
                                else:
                                    logger.warning(f"Skipped unavailable tool: {tool_name} for agent: {agent_data.name}")
                    
                    # Create the agent with tools
                    agent = Agent(
                        role=agent_data.role,
                        goal=agent_data.goal,
                        backstory=agent_data.backstory,
                        verbose=True,
                        allow_delegation=agent_data.allow_delegation,
                        tools=tools
                    )
                    
                    # Set model if specified
                    if hasattr(agent_data, 'llm') and agent_data.llm:
                        # Don't try to set agent.model - recreate the agent with the llm parameter
                        agent = Agent(
                            role=agent_data.role,
                            goal=agent_data.goal,
                            backstory=agent_data.backstory,
                            verbose=True,
                            allow_delegation=agent_data.allow_delegation,
                            tools=tools,
                            llm=agent_data.llm  # Pass llm as a parameter during initialization
                        )
                        logger.info(f"Set agent LLM to: {agent_data.llm}")
                
                # Now, create the task with the proper agent
                if not task_data:
                    # Create a default task with the agent we've just created
                    task = Task(
                        description=task_description,
                        expected_output=task_expected_output,
                        agent=agent
                    )
                else:
                    # Create task from database data
                    logger.info(f"Creating task from database data: {task_data.name}")
                    
                    # Get tools for the task
                    tools = []
                    if task_data.tools:
                        for tool_id in task_data.tools:
                            tool_record = db.query(ToolModel).filter(ToolModel.id == tool_id).first()
                            if tool_record:
                                tool_name = tool_record.title
                                tool = tool_factory.create_tool(tool_name)
                                if tool:
                                    tools.append(tool)
                                    logger.info(f"Added tool: {tool_name} to task: {task_data.name}")
                                else:
                                    logger.warning(f"Skipped unavailable tool: {tool_name} for task: {task_data.name}")
                    
                    # Create task with tools and agent
                    task = Task(
                        description=task_data.description,
                        expected_output=task_data.expected_output,
                        agent=agent,
                        tools=tools
                    )
            
            finally:
                db.close()
            
            # Extract API keys from config for direct use
            openai_api_key = self._config.get('openai_api_key')
            perplexity_api_key = self._config.get('perplexity_api_key')
            serper_api_key = self._config.get('serper_api_key')
            
            # Don't create LangChain's ChatOpenAI - it's not compatible with CrewAI
            # Instead, let CrewAI create its own LLM with the API key
            
            # Create a crew for the start point
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True,
                process=Process.sequential,
                openai_api_key=openai_api_key,
                perplexity_api_key=perplexity_api_key,
                serper_api_key=serper_api_key
            )
            
            # Set up streaming callback for the crew if available
            if streaming_cb:
                # Enable verbose output for all components
                crew.process.verbose = True
                crew.process.output_callback = streaming_cb.execute
                
                # Enable verbose mode and callbacks for all tasks and agents
                for task in crew.tasks:
                    # Enable verbose mode and callback for task process
                    if hasattr(task, 'process'):
                        task.process.verbose = True
                        task.process.output_callback = streaming_cb.execute
                    
                    # Enable verbose mode and callback for agent process
                    if hasattr(task, 'agent'):
                        agent = task.agent
                        if hasattr(agent, 'process'):
                            agent.process.verbose = True
                            agent.process.output_callback = streaming_cb.execute
                        
                        # Enable verbose mode and callback for tool processes
                        if hasattr(agent, 'tools'):
                            for tool in agent.tools:
                                if hasattr(tool, 'process'):
                                    tool.process.verbose = True
                                    tool.process.output_callback = streaming_cb.execute
                
                logger.info("Enabled streaming callbacks for all components")
            
            # Define a proper Flow class with @start decorator
            class DynamicFlow(CrewAIFlow):
                @start()
                def start_flow(self):
                    logger.info(f"Starting flow with {crew_name} crew and {task_name} task")
                    result = crew.kickoff()
                    return result
            
            # Create an instance of our properly defined flow
            flow_instance = DynamicFlow()
            logger.info("Flow configured successfully with proper @start method")
            return flow_instance
            
        except Exception as e:
            logger.error(f"Error creating flow: {e}", exc_info=True)
            raise ValueError(f"Failed to create flow: {str(e)}")

    async def kickoff(self) -> Dict[str, Any]:
        """Execute the flow and return results"""
        logger.info(f"Kicking off flow for job {self._job_id}")
        
        flow_instance = self.flow()
        
        try:
            # Execute the flow using kickoff_async directly, not asyncio.run()
            result = await flow_instance.kickoff_async()
            
            logger.info(f"Flow execution completed successfully for job {self._job_id}")
            return {
                "success": True,
                "result": result,
                "flow_id": self._flow_id
            }
        except Exception as e:
            logger.error(f"Error executing flow: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "flow_id": self._flow_id
            } 