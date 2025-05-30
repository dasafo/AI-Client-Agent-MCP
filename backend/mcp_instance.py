# backend/mcp_instance.py
# Definition of the central Master Control Program (MCP) instance

import logging

# Configure logger
logger = logging.getLogger(__name__)

# Try to import FastMCP from fastmcp or mcp
try:
    from fastmcp import FastMCP
    logger.info("Successfully imported FastMCP from 'fastmcp' package")
except ImportError:
    try:
        from mcp import FastMCP
        logger.info("Successfully imported FastMCP from 'mcp' package")
    except ImportError:
        logger.critical("CRITICAL ERROR: Could not import FastMCP from either 'fastmcp' or 'mcp'")
        logger.critical("Make sure one of these packages is correctly installed in your environment")
        raise

# Create a unique FastMCP instance for the entire application
# This centralized instance allows registering all tools and handling client requests
mcp = FastMCP(
    "AI-Client-Agent-MCP",  # Name of the MCP agent
    stateless_http=True,    # Configuration for stateless HTTP handling
)

# # Optionally, expose the FastAPI app directly for Uvicorn
# app = mcp.app
