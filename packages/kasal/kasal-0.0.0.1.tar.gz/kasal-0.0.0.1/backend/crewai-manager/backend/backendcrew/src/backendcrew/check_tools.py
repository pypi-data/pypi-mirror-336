from .database import SessionLocal, Tool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_tools():
    db = SessionLocal()
    try:
        tools = db.query(Tool).all()
        logger.info(f"Found {len(tools)} tools in database")
        for tool in tools:
            logger.info(f"Tool: {tool.title} - {tool.icon}")
        return tools
    except Exception as e:
        logger.error(f"Error checking tools: {e}")
        return []
    finally:
        db.close()

if __name__ == "__main__":
    check_tools() 