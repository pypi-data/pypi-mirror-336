from fastapi import APIRouter

router = APIRouter()

# Import routers from modules
from .logs import router as logs_router
from .generate_crew import router as generation_router
from .generate_agent import router as agent_router
from .generate_task import router as task_generation_router
from .generate_connections import router as connections_router
from .generate_templates import router as templates_router
from .agents import router as agents_router
from .tasks import router as tasks_router
from .jobs import router as jobs_router
from .runs import router as runs_router
from .tools import router as tools_router
from .uc_tools import router as uc_tools_router
from .keys import router as keys_router
from .recipes import router as recipes_router
from .crew_store import router as crews_router
from .flow_store import router as flows_router
from .databricks import router as databricks_router
from .schedules import router as schedules_router
from .task_statuses import router as task_statuses_router
from .upload import router as upload_router
from .memory import router as memory_router

# Add all routers
router.include_router(logs_router, prefix="/llm-logs", tags=["Logs"])
router.include_router(generation_router, prefix="/generate", tags=["Generation"])
router.include_router(agent_router, prefix="/generate", tags=["Generate Agent"])
router.include_router(task_generation_router, prefix="/generate", tags=["Generate Task"])
router.include_router(connections_router, prefix="/generate", tags=["Generate Connections"])
router.include_router(templates_router, prefix="/generate", tags=["Generate Templates"])
router.include_router(agents_router, prefix="/agents", tags=["Agents"])
router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
router.include_router(runs_router, prefix="/runs", tags=["Runs"])
router.include_router(tools_router, prefix="/tools", tags=["Tools"])
router.include_router(uc_tools_router, prefix="/uc-tools", tags=["UC Tools"])
router.include_router(keys_router, prefix="/keys", tags=["Keys"])
router.include_router(recipes_router, prefix="/recipes", tags=["Recipes"])
router.include_router(crews_router, prefix="/crews", tags=["Crews"])
router.include_router(flows_router, prefix="/flows", tags=["Flows"])
router.include_router(databricks_router, prefix="/databricks", tags=["Databricks"])
router.include_router(schedules_router, prefix="/schedules", tags=["Schedules"])
router.include_router(task_statuses_router, prefix="/task-statuses", tags=["Task Statuses"])
router.include_router(upload_router, prefix="/upload", tags=["File Upload"])
router.include_router(memory_router, prefix="/memory", tags=["Memory"])