"""Task conditions for CrewAI tasks."""

import logging
from crewai.tasks.task_output import TaskOutput

logger = logging.getLogger(__name__)

def is_data_missing(output: TaskOutput) -> bool:
    """
    Check if the output has less than 10 items.
    
    Args:
        output: The TaskOutput to evaluate
        
    Returns:
        bool: True if data is missing, False otherwise
    """
    logger.info("=== is_data_missing function called ===")
    logger.info(f"TaskOutput type: {type(output)}")
    
    if not hasattr(output, 'pydantic'):
        logger.info("No pydantic model found in output, returning True")
        return True
    
    logger.info(f"Pydantic model: {output.pydantic}")
    logger.info(f"Checking events length in: {output.pydantic.events}")
    events_count = len(output.pydantic.events)
    result = events_count < 10
    
    logger.info(f"Found {events_count} events. Need at least 10.")
    logger.info(f"Is data missing? {result}")
    return result 