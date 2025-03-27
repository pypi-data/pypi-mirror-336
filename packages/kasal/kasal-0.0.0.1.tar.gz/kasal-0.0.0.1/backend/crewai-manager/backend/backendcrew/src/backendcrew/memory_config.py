"""
Memory configuration module for CrewAI agents and crews.

This module provides utilities to configure and manage memory settings
for CrewAI agents, including short-term, long-term, and entity memory.
"""

import os
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# Configure logging
logger = logging.getLogger(__name__)

# Get the absolute path to the project directory
current_dir = Path(__file__).parent  # /src/backendcrew
project_root = current_dir.parent.parent  # Go up to the project root

# Define memory storage directory
MEMORY_DIR = Path(os.environ.get('CREWAI_STORAGE_DIR', project_root / 'memory'))
os.makedirs(MEMORY_DIR, exist_ok=True)

logger.info(f"Memory directory initialized at: {MEMORY_DIR}")

class MemoryConfig:
    """Memory configuration for CrewAI agents and crews."""
    
    DEFAULT_EMBEDDER = {
        'provider': 'openai',
        'config': {
            'model': 'text-embedding-3-small'
        }
    }
    
    @staticmethod
    def setup_memory_components(
        crew_name: str = "default_crew",
        memory_enabled: bool = True,
        embedder_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Set up memory components for a crew.
        
        Args:
            crew_name: Name to use for the crew's memory storage
            memory_enabled: Whether memory is enabled for this crew
            embedder_config: Configuration for the embedding model
            
        Returns:
            dict: Memory configuration dictionary with long-term,
                 short-term, and entity memory components
        """
        if not memory_enabled:
            logger.info(f"Memory is disabled for crew '{crew_name}'")
            return {'memory': False}
            
        # Use default embedder if none provided
        embedder = embedder_config or MemoryConfig.DEFAULT_EMBEDDER
        logger.info(f"Setting up memory for crew '{crew_name}' with embedder: {embedder['provider']}")
        
        # Create memory storage paths
        crew_memory_dir = MEMORY_DIR / crew_name
        os.makedirs(crew_memory_dir, exist_ok=True)
        
        memory_path = str(crew_memory_dir)
        db_path = str(crew_memory_dir / "long_term_memory.db")
        
        logger.info(f"Memory storage path: {memory_path}")
        logger.info(f"Database path: {db_path}")
        
        # Set up memory components
        try:
            memory_config = {
                'memory': True,
                'long_term_memory': LongTermMemory(
                    storage=LTMSQLiteStorage(
                        db_path=db_path
                    )
                ),
                'short_term_memory': ShortTermMemory(
                    storage=RAGStorage(
                        embedder_config=embedder,
                        type="short_term",
                        path=memory_path
                    )
                ),
                'entity_memory': EntityMemory(
                    storage=RAGStorage(
                        embedder_config=embedder,
                        type="entity",
                        path=memory_path
                    )
                ),
                'embedder': embedder  # Add embedder as a simpler way to configure the embedding model
            }
            
            logger.info(f"Memory components set up successfully for crew '{crew_name}'")
            return memory_config
        except Exception as e:
            logger.error(f"Error setting up memory components: {e}", exc_info=True)
            # Fallback to basic memory configuration
            return {'memory': True}
            
    @staticmethod
    def get_agent_memory_config(agent_config: Dict[str, Any]) -> tuple:
        """
        Extract memory configuration from agent config.
        
        Args:
            agent_config: Agent configuration dictionary
            
        Returns:
            tuple: (memory_enabled, embedder_config)
        """
        memory_enabled = agent_config.get('memory', True)
        embedder_config = agent_config.get('embedder_config', MemoryConfig.DEFAULT_EMBEDDER)
        
        return memory_enabled, embedder_config
    
    @staticmethod
    def list_crew_memories() -> List[str]:
        """
        List all crew memory directories.
        
        Returns:
            List[str]: List of crew names with memory storage
        """
        if not MEMORY_DIR.exists():
            return []
            
        return [d.name for d in MEMORY_DIR.iterdir() if d.is_dir()]
    
    @staticmethod
    def reset_crew_memory(crew_name: str) -> bool:
        """
        Reset memory for a specific crew.
        
        Args:
            crew_name: Name of the crew to reset memory for
            
        Returns:
            bool: True if successful, False otherwise
        """
        crew_dir = MEMORY_DIR / crew_name
        if not crew_dir.exists():
            logger.warning(f"No memory found for crew '{crew_name}'")
            return False
            
        try:
            # Remove and recreate the directory
            shutil.rmtree(crew_dir)
            os.makedirs(crew_dir, exist_ok=True)
            logger.info(f"Memory reset for crew '{crew_name}'")
            return True
        except Exception as e:
            logger.error(f"Error resetting memory for crew '{crew_name}': {e}")
            return False
    
    @staticmethod
    def reset_all_memories() -> bool:
        """
        Reset all crew memories.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not MEMORY_DIR.exists():
            logger.warning("Memory directory does not exist")
            return False
            
        try:
            # Get all crew directories
            crew_dirs = [d for d in MEMORY_DIR.iterdir() if d.is_dir()]
            
            # Reset each crew's memory
            for crew_dir in crew_dirs:
                shutil.rmtree(crew_dir)
                os.makedirs(crew_dir, exist_ok=True)
                logger.info(f"Memory reset for crew '{crew_dir.name}'")
                
            logger.info(f"All memories reset successfully ({len(crew_dirs)} crews)")
            return True
        except Exception as e:
            logger.error(f"Error resetting all memories: {e}")
            return False 