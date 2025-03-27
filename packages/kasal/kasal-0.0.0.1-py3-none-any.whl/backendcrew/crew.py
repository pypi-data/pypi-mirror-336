"""
Unified Crew implementation that combines the functionality of regular and dynamic crews.
"""
import logging
import os
from typing import Dict, Type, List, Optional
from pathlib import Path
from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task
from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput
from sqlalchemy.orm import Session

from .utils.logger_manager import LoggerManager
from .utils.crew_helpers import create_agent, create_task, is_data_missing
from .llm_config import LLMConfig, ModelProvider, SUPPORTED_MODELS
from .memory_config import MemoryConfig
from .tools.tool_factory import ToolFactory
from .tools.tool_schemas import TOOL_OUTPUT_MODELS
from .database import SessionLocal, Run, Agent as AgentModel, Crew as CrewModel

# Initialize logger manager
logger_manager = LoggerManager()

# Configure standard logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define uploads directory for knowledge files
UPLOADS_DIR = Path(os.environ.get('KNOWLEDGE_DIR', 'uploads/knowledge'))

class Backendcrew:
	"""Base Backendcrew class that can be used with standard or dynamic configurations"""

	def __init__(self, job_id: Optional[str] = None, agents_yaml: Optional[Dict] = None, tasks_yaml: Optional[Dict] = None):
		"""
		Initialize a new Backendcrew instance.
		
		Args:
			job_id: Optional job ID for dynamic crews
			agents_yaml: Optional agents configuration
			tasks_yaml: Optional tasks configuration
		"""
		self._agents_config = agents_yaml
		self._tasks_config = tasks_yaml
		self._job_id = job_id
		self._output_dir = None
		self._config = {
			'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY'),
			'openai_api_key': LLMConfig.get_api_key(),
			'serper_api_key': os.getenv('SERPER_API_KEY'),
		}
		self._memory_enabled = True  # Default memory state
		self._memory_config = MemoryConfig.DEFAULT_EMBEDDER
		logger.info(f"Initializing Backendcrew{' for job ' + job_id if job_id else ''}")

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

	@property
	def agents_config(self):
		return self._agents_config

	@agents_config.setter
	def agents_config(self, value):
		logger.info(f"Setting agents_config: {type(value)}")
		self._agents_config = value

	@property
	def tasks_config(self):
		return self._tasks_config

	@tasks_config.setter
	def tasks_config(self, value):
		logger.info(f"Setting tasks_config: {type(value)}")
		self._tasks_config = value
		
	@property
	def memory_enabled(self):
		return self._memory_enabled
		
	@memory_enabled.setter
	def memory_enabled(self, value):
		self._memory_enabled = value

	@property
	def memory_config(self):
		return self._memory_config
		
	@memory_config.setter
	def memory_config(self, value):
		self._memory_config = value
		
	def _process_knowledge_sources(self, agent_config):
		"""
		Process knowledge sources to handle uploaded files.
		If a knowledge source path doesn't have a full path,
		check if it exists in the uploads directory.
		"""
		if 'knowledge_sources' not in agent_config or not agent_config['knowledge_sources']:
			return agent_config
			
		processed_sources = []
		for source in agent_config['knowledge_sources']:
			if source['type'] in ['file', 'pdf', 'csv', 'excel', 'json'] and not os.path.isabs(source['source']):
				# Check if the file exists in the uploads directory
				uploads_path = UPLOADS_DIR / source['source']
				if uploads_path.exists():
					logger.info(f"Found uploaded file: {uploads_path}")
					source['source'] = str(uploads_path)
				else:
					logger.warning(f"File not found in uploads directory: {source['source']}")
			processed_sources.append(source)
			
		agent_config['knowledge_sources'] = processed_sources
		return agent_config

	def crew(self) -> Crew:
		"""Creates the crew based on configurations"""
		logger.debug("Starting crew creation with:")
		logger.debug(f"Agents config: {self.agents_config}")
		logger.debug(f"Tasks config: {self.tasks_config}")
		
		try:
			agents = {}
			tasks = []
			crew_name = f"crew_{self._job_id}" if self._job_id else "default_crew"

			# First create all agents
			for agent_key, agent_config in self.agents_config.items():
				logger.debug(f"Creating agent {agent_key} with config: {agent_config}")
				
				# Ensure model is specified in agent config
				if 'model' not in agent_config:
					agent_config['model'] = LLMConfig.get_default_model()
				logger.info(f"Agent {agent_key} will use model: {agent_config['model']}")
				
				# Process knowledge sources to handle uploaded files
				agent_config = self._process_knowledge_sources(agent_config)
				
				# Extract memory configuration from agent config
				memory_enabled, embedder_config = MemoryConfig.get_agent_memory_config(agent_config)
				self.memory_enabled = memory_enabled
				
				if embedder_config:
					self.memory_config = embedder_config
				
				# Create the agent with the model - providers will be handled dynamically
				agents[agent_key] = create_agent(agent_key, agent_config, self.config)
				logger.debug(f"Created agent {agent_key}: {agents[agent_key]}")

			# Then create tasks with their assigned agents
			for task_key, task_config in self.tasks_config.items():
				agent_key = task_config.get('agent')
				logger.info(f"Creating task {task_key} for agent {agent_key}")
				
				if agent_key not in agents:
					logger.error(f"Agent '{agent_key}' not found for task '{task_key}'")
					raise ValueError(f"Agent '{agent_key}' not found for task '{task_key}'")
				
				# Create either conditional or regular task
				if task_config.get('condition') == 'data_is_missing':
					logger.info(f"Creating conditional task for {task_key} with condition: data_is_missing")
					try:
						task = ConditionalTask(
							description=task_config['description'],
							expected_output=task_config['expected_output'],
							agent=agents[agent_key],
							condition=is_data_missing,
							context=task_config.get('context', []),
							output_pydantic=task_config.get('output_pydantic'),
							tools=task_config.get('tools', []),
							async_execution=task_config.get('async_execution', False),
							output_file=task_config.get('output_file'),
							output_json=task_config.get('output_json'),
							human_input=task_config.get('human_input', False),
							retry_on_fail=task_config.get('retry_on_fail', True),
							max_retries=task_config.get('max_retries', 3),
							timeout=task_config.get('timeout'),
							priority=task_config.get('priority', 0),
							error_handling=task_config.get('error_handling', 'default'),
							cache_response=task_config.get('cache_response', False),
							cache_ttl=task_config.get('cache_ttl', 3600),
							callback=task_config.get('callback')
						)
						logger.info(f"Conditional task created: {task}")
						logger.info(f"Task condition: {task.condition}")
					except Exception as e:
						logger.error(f"Error creating conditional task: {e}", exc_info=True)
						raise
				else:
					task = create_task(task_key, task_config, agents[agent_key], self.output_dir, self.config)
				
				tasks.append(task)
				logger.info(f"Created task {task_key} with callback: {task_config.get('callback')}")

			# Set up memory using the memory_config module
			memory_settings = MemoryConfig.setup_memory_components(
				crew_name=crew_name,
				memory_enabled=self.memory_enabled,
				embedder_config=self.memory_config
			)

			# Default Crew parameters
			crew_kwargs = {
				'agents': list(agents.values()),
				'tasks': tasks,
				'process': Process.sequential,
				'verbose': True,
				**memory_settings
			}

			# For dynamic crews with job_id, set up planning parameters
			if self._job_id:
				# Get planning configuration from Run table
				db = SessionLocal()
				try:
					run = db.query(Run).filter(Run.job_id == self._job_id).first()
					if run:
						# Add planning parameters
						planning_enabled = run.planning
						crew_kwargs['planning'] = planning_enabled
						logger.info(f"Planning enabled for job {self._job_id}: {planning_enabled}")

						# Get the model from the inputs
						model = run.inputs.get('model')
						if not model:
							logger.warning("No model specified in inputs, using default gpt-4o-mini")
							model = 'gpt-4o-mini'
						logger.info(f"Using model for planning: {model}")
						
						# Add model parameters to crew
						crew_kwargs['planning_llm'] = model
						crew_kwargs['llm'] = model
				finally:
					db.close()

			# Create and return the crew
			crew = Crew(**crew_kwargs)
			logger.info("Crew created successfully with:")
			logger.info(f"Number of agents: {len(crew.agents)}")
			logger.info(f"Number of tasks: {len(crew.tasks)}")
			logger.info(f"Memory enabled: {self.memory_enabled}")
			logger.info(f"Memory provider: {self.memory_config.get('provider', 'openai')}")
			logger.info("Task details:")
			for task in crew.tasks:
				logger.info(f"- Task: {task.description}")
				logger.info(f"  Has callback: {hasattr(task, 'callback') and task.callback is not None}")
				if isinstance(task, ConditionalTask):
					logger.info(f"  Conditional task with condition: {task.condition.__name__}")
				
				# Log agent model information
				if hasattr(task, 'agent') and task.agent:
					# Use role instead of name, as Agent objects in CrewAI don't have a name attribute
					agent_role = getattr(task.agent, 'role', 'Unknown agent')
					logger.info(f"  Agent role: {agent_role}")
					if hasattr(task.agent, 'model'):
						logger.info(f"  Agent model: {task.agent.model}")
					else:
						logger.info(f"  Agent model: unknown")
			
			return crew
		except Exception as e:
			logger.error(f"Error creating crew: {e}", exc_info=True)
			raise
