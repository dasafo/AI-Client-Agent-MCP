import sys
import os
from pathlib import Path
from backend.core.config import SERVER_HOST, SERVER_PORT
from backend.core.logging import get_logger
from backend.mcp_instance import mcp
from backend.api.v1.tools import client_tools
from backend.api.v1.tools import invoice_tools
from backend.api.v1.tools import report_tools

# Main server file for AI Client Agent MCP
# Configures and starts the FastMCP server with all registered tools

logger = get_logger(__name__)

# Logs directory setup
LOGS_DIR = Path("/app/logs")
LOGS_DIR.mkdir(exist_ok=True, parents=True)

# File handlers for logging
try:
    # Configure file logging
    import logging
    file_handler = logging.FileHandler(LOGS_DIR / "server.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
    logger.addHandler(file_handler)
    
    # Log startup details
    logger.info("Server starting up...")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Virtual environment: {os.environ.get('VIRTUAL_ENV')}")
except IOError as e:
    logger.warning(f"Could not set up file logging: {e}")

HOST = SERVER_HOST
PORT = SERVER_PORT

if __name__ == "__main__":
    # Main entry point when script is executed directly
    logger.info(f"Starting FastMCP on {HOST}:{PORT}...")
    # Tools are automatically registered by FastMCP when imported
    # if they are decorated with @mcp.tool in the imported modules
    mcp.run(
        transport="sse",  # Server-Sent Events as transport mechanism
        host=HOST,
        port=PORT,
        path="/sse",  # Path for SSE connection
        log_level="info",  # Log detail level
    )

# Example command to run the server:
#  /home/david/Documents/AI/AI-Client-Agent-MCP/.venv/bin/python -m backend.server 
