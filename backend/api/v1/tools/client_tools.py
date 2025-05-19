"""
Client tools module for MCP API.
These tools expose client-related functionality callable via the MCP API.
"""

import logging
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from backend.services.client_service import ClientService
from backend.models.client import ClientCreate

# Logging configuration
logger = logging.getLogger(__name__)


async def search_client_by_email(email: str, ctx: Context) -> Dict[str, Any]:
    """
    Search for a client by email address using the service.
    """
    try:
        if ctx is None or ctx.request_context is None:
            return {"error": "Invalid or missing context"}
        pool = ctx.request_context.lifespan_context
        client_service = ClientService(pool)
        client = await client_service.get_client_by_email(email)
        if not client:
            return {"error": f"No client found with email {email}"}
        return client
    except Exception as e:
        logger.error(f"Error searching client by email {email}: {str(e)}")
        return {"error": "Error searching for client"}


async def add_client(
    name: str,
    email: str,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Add a new client to the database using the service.
    """
    if ctx is None or ctx.request_context is None:
        return {"error": "Invalid or missing context"}
    pool = ctx.request_context.lifespan_context
    client_service = ClientService(pool)
    # Uniqueness and format validation here
    existing = await client_service.get_client_by_email(email)
    if existing:
        return {"error": f"Email {email} is already registered"}
    client_obj = ClientCreate(name=name, email=email, phone=phone, city=city)
    created = await client_service.create_client(client_obj)
    return {"success": True, "client": created}


def register_tools(mcp: FastMCP) -> None:
    """
    Register tools in the MCP instance.
    """
    mcp.add_tool(
        search_client_by_email,
        name="search_client_by_email",
        description="Search for a client by email address",
    )
    mcp.add_tool(
        add_client,
        name="add_client",
        description="Add a new client to the database",
    )
