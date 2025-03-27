"""
Utilities for event loop management and handling asyncio operations across threads.
"""
import asyncio
import logging
from typing import Any, Callable, List

from ..utils.logger_manager import LoggerManager

# Initialize logger manager
logger_manager = LoggerManager()

def create_and_run_loop(coroutine: Any) -> Any:
    """Create a new event loop, run the coroutine, and clean up properly."""
    new_loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(new_loop)
        result = new_loop.run_until_complete(coroutine)
        return result
    finally:
        # Properly clean up the event loop
        try:
            # Close all running event loop tasks
            pending = asyncio.all_tasks(new_loop) if hasattr(asyncio, 'all_tasks') else []
            for task in pending:
                task.cancel()
            # Run the event loop until all tasks are canceled
            if pending:
                new_loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            # Remove the loop from the current context and close it
            asyncio.set_event_loop(None)
            new_loop.close()
        except Exception as e:
            logger_manager.crew.error(f"Error cleaning up event loop: {str(e)}")

def create_task_lifecycle_callback(loop_handler: Callable, callbacks: List, task_key: str) -> Callable:
    """Create a callback for task lifecycle events with proper event loop handling."""
    def callback_function(task_obj, success=True):
        logger_manager.crew.info(f"Task event for {task_key} (success: {success})")
        # Create a new event loop for the callback
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            for callback in callbacks:
                try:
                    if hasattr(callback, loop_handler):
                        logger_manager.crew.info(f"Calling {loop_handler} for {callback.__class__.__name__}")
                        handler = getattr(callback, loop_handler)
                        if loop_handler == 'on_task_end':
                            new_loop.run_until_complete(handler(task_obj, success))
                        else:
                            new_loop.run_until_complete(handler(task_obj))
                except Exception as callback_error:
                    logger_manager.crew.error(f"Error in {loop_handler}: {callback_error}")
                    logger_manager.crew.error("Stack trace:", exc_info=True)
                    # Continue with other callbacks even if one fails
        finally:
            # Properly clean up the event loop
            try:
                # Close all running event loop tasks
                pending = asyncio.all_tasks(new_loop) if hasattr(asyncio, 'all_tasks') else []
                for task in pending:
                    task.cancel()
                # Run the event loop until all tasks are canceled
                if pending:
                    new_loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                # Remove the loop from the current context and close it
                asyncio.set_event_loop(None)
                new_loop.close()
            except Exception as e:
                logger_manager.crew.error(f"Error cleaning up {loop_handler} event loop: {str(e)}")
    
    return callback_function

def run_in_thread_with_loop(func: Callable, *args, **kwargs) -> Any:
    """Run a function in a thread with a properly managed event loop."""
    # Track whether we created a new event loop
    created_loop = False
    loop = None
    
    try:
        # Set up event loop for this thread
        try:
            # Try to get the current event loop
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # If there's no event loop in this thread, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            created_loop = True
            logger_manager.crew.info("Created new event loop for thread execution")

        # Execute the function
        return func(*args, **kwargs)
    
    finally:
        # Clean up the event loop only if we created it
        if created_loop and loop is not None:
            try:
                # Only close the loop if we created it
                asyncio.set_event_loop(None)
                loop.close()
                logger_manager.crew.info("Successfully closed the event loop created for this thread")
            except Exception as e:
                logger_manager.crew.error(f"Error cleaning up event loop: {str(e)}") 