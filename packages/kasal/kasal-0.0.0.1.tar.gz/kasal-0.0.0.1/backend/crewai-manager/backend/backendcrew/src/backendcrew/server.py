import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio
from contextlib import asynccontextmanager
from .database import init_db, get_async_db
from .api.schedules import check_and_run_schedules
from .utils.logger_manager import LoggerManager
import sqlite3
import subprocess
import sys

# Disable OpenTelemetry instrumentation
os.environ["OTEL_SDK_DISABLED"] = "true"

# Get the absolute path to the .env file
current_dir = Path(__file__).parent  # /src/backendcrew
project_root = current_dir.parent.parent  # Go up to backendcrew root
env_path = project_root / '.env'

# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Get LoggerManager instance and initialize it
logger_manager = LoggerManager.get_instance(str(project_root / 'logs'))
system_logger = logger_manager.system
scheduler_logger = logger_manager.scheduler
api_logger = logger_manager.api
access_logger = logger_manager.access

# Import router after environment variables are loaded
from .api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database
    await init_db()
    system_logger.info("Database initialized")
    
    # Check and populate tools if needed
    db_path = str(current_dir / 'crewai.db')
    await populate_tools_if_needed(db_path)
    
    # Start the scheduler in the background
    async for db in get_async_db():
        asyncio.create_task(check_and_run_schedules(db))
        scheduler_logger.info("Schedule checker started")
        break
    
    yield
    # Clean up code here if needed

# Replace the app definition with one that uses the lifespan
app = FastAPI(title="Backendcrew API", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add cache control middleware
@app.middleware("http")
async def add_cache_control_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Include the router
app.include_router(router, prefix="/api")

# Mount the build directory
def find_build_path():
    # When installed as a package, the files will be in the package directory
    package_dir = Path(__file__).resolve().parent
    build_path = package_dir / "static" / "build"
    system_logger.info(f"Looking for build files in package at: {build_path}")
    
    if not build_path.exists():
        system_logger.error(f"Build directory not found at {build_path}")
        raise RuntimeError(f"Build directory not found at {build_path}. Make sure the package was built correctly.")
    
    return build_path

# Function to check if tools exist in the database
async def check_tools_exist(db_path):
    try:
        # Check if database file exists
        if not os.path.exists(db_path):
            system_logger.info(f"Database file does not exist at {db_path}")
            return False
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tools table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tools'")
        if not cursor.fetchone():
            system_logger.info("Tools table does not exist")
            return False
            
        # Check if tools table has any rows
        cursor.execute("SELECT COUNT(*) FROM tools")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except sqlite3.Error as e:
        system_logger.error(f"Error checking for tools: {e}")
        return False

# Function to find the scripts directory
def find_scripts_directory():
    """Find the scripts directory by searching up from the current file."""
    # Start with the directory of the current file
    current_path = Path(__file__).resolve().parent
    
    # Try to find the workspace root by looking for common markers
    workspace_markers = [
        ".git",           # Git repository marker
        "README.md",      # Common project file
        "pyproject.toml", # Python project marker
        "setup.py",       # Python package marker
    ]
    
    # Keep track of attempts to avoid infinite loops
    max_attempts = 15
    attempts = 0
    workspace_root = None
    
    # First try to find the workspace root
    search_path = current_path
    while attempts < max_attempts and search_path != search_path.parent:
        # Check if any of the workspace markers exist
        for marker in workspace_markers:
            if (search_path / marker).exists():
                workspace_root = search_path
                system_logger.info(f"Found workspace root at: {workspace_root}")
                break
        
        if workspace_root:
            break
            
        # Move up one level
        search_path = search_path.parent
        attempts += 1
    
    # Reset attempts
    attempts = 0
    
    # Priority-ordered list of possible script directory locations
    possible_locations = []
    
    # If we found the workspace root, add those paths first
    if workspace_root:
        possible_locations.extend([
            workspace_root / "backend" / "scripts",
            workspace_root / "scripts",
            workspace_root / "tools",
            workspace_root / "backend" / "tools",
        ])
    
    # Add relative paths from the current file
    possible_locations.extend([
        current_path / "scripts",
        current_path.parent / "scripts",
        current_path.parent.parent / "scripts",
        current_path.parent.parent.parent / "backend" / "scripts",
    ])
    
    # Check all possible locations in order
    for location in possible_locations:
        if location.exists() and (location / "populate_tools.py").exists():
            system_logger.info(f"Found scripts directory at: {location}")
            return location
    
    # If we're really desperate, try navigating up the directory tree
    search_path = current_path
    while attempts < max_attempts and search_path != search_path.parent:
        # Check various possibilities at each level
        candidates = [
            search_path / "scripts",
            search_path / "tools",
            search_path.parent / "backend" / "scripts",
            search_path.parent / "scripts",
        ]
        
        for candidate in candidates:
            if candidate.exists() and (candidate / "populate_tools.py").exists():
                system_logger.info(f"Found scripts directory at: {candidate}")
                return candidate
        
        # Move up one level
        search_path = search_path.parent
        attempts += 1
    
    # If we couldn't find it, return None
    return None

def find_populate_script():
    """Find the populate_tools.py script in the package's scripts directory."""
    current_path = Path(__file__).resolve().parent
    system_logger.info(f"Starting search from current path: {current_path}")
    
    # Look for populate_tools.py in the package's scripts directory
    scripts_dir = current_path / "scripts"
    populate_script = scripts_dir / "populate_tools.py"
    
    system_logger.info(f"Looking for script at: {populate_script}")
    system_logger.info(f"Scripts directory exists: {scripts_dir.exists()}")
    if scripts_dir.exists():
        system_logger.info(f"Script file exists: {populate_script.exists()}")
    
    if populate_script.exists():
        system_logger.info(f"Found populate_tools.py at: {populate_script}")
        return scripts_dir
    
    system_logger.error("Could not find populate_tools.py in the package's scripts directory")
    return None

# Function to populate tools if they don't exist
async def populate_tools_if_needed(db_path):
    if not await check_tools_exist(db_path):
        system_logger.info("No tools found in database, populating tools...")
        
        # Ensure database exists by creating it
        try:
            conn = sqlite3.connect(db_path)
            conn.close()
            system_logger.info(f"Created database at {db_path}")
        except Exception as e:
            system_logger.error(f"Failed to create database: {e}")
            return
        
        # Try to find the populate_tools.py script
        scripts_dir = find_populate_script()  # Use the new function instead
        if not scripts_dir:
            system_logger.error("Could not find scripts directory containing populate_tools.py")
            return
            
        populate_script = scripts_dir / "populate_tools.py"
        system_logger.info(f"Using populate_tools script at: {populate_script}")
        
        if not populate_script.exists():
            system_logger.error(f"Populate tools script not found at {populate_script}")
            return
        
        try:
            # Run the populate_tools.py script with the database path
            result = subprocess.run(
                [sys.executable, str(populate_script), db_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                system_logger.info(f"Successfully populated tools: {result.stdout}")
            else:
                system_logger.error(f"Failed to populate tools: {result.stderr}")
        except Exception as e:
            system_logger.error(f"Error while running populate_tools.py: {e}")

try:
    build_path = find_build_path()
    system_logger.info(f"Using build path: {build_path}")
    app.mount("/static", StaticFiles(directory=str(build_path / "static"), html=True), name="static")
except Exception as e:
    system_logger.error(f"Failed to mount static files: {e}")
    raise

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Serve index.html for any path that wasn't matched by the static files
    return FileResponse(str(build_path / "index.html"))

def main():
    """Main entry point for the server."""
    uvicorn.run(
        "backendcrew.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()