from backend.mcp_instance import mcp
from backend.services.client_service import (
    get_all_clients as service_get_all_clients,
    create_client as service_create_client, 
    update_client as service_update_client, 
    get_client_by_id as service_get_client_by_id,
    delete_client as service_delete_client
)
from backend.models.client import (
    ClientCreate, 
    ClientUpdate, 
    ClientOut, 
    ClientDeleteResponse
)
from typing import List, Dict, Any
from datetime import datetime
from backend.core.database import database
from backend.core.logging import get_logger

logger = get_logger(__name__)

# Tools for client management
# These functions expose client management functionality through the MCP (Master Control Program)

@mcp.tool(
    name="list_clients",
    description="List clients from the database",
)
async def list_clients() -> dict:
    """List clients from the database"""
    try:
        # Get all clients from the service
        clients_data = await service_get_all_clients()
        if isinstance(clients_data, dict) and not clients_data.get("success", True):
            logger.error(f"Error listing clients: {clients_data.get('error', clients_data)}")
            return clients_data
        processed_clients = []
        
        # Process each client to handle dates correctly
        for client_dict in clients_data:
            processed_clients.append(ClientOut(**client_dict))
            
        # Return the serialized list of clients
        logger.debug(f"TOOL list_clients response: {[c.model_dump() for c in processed_clients]}")
        return {"success": True, "clients": [c.model_dump() for c in processed_clients]}
    except Exception as e:
        # Catch any error and return it in the response
        logger.error(f"Unexpected error in list_clients: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="get_client",
    description="Get a client by its ID",
)
async def get_client(client_id: int) -> dict:
    """
    Get a client by its ID
    
    Args:
        client_id: ID of the client to query
    """
    try:
        # Search for the client by its ID using the service
        client_data = await service_get_client_by_id(client_id)
        if not client_data:
            # If the client is not found, return an error message
            logger.warning(f"Client with ID {client_id} not found")
            return {"success": False, "error": f"Client with ID {client_id} not found"}
        
        if isinstance(client_data, dict) and not client_data.get("success", True):
            logger.error(f"Error getting client: {client_data.get('error', client_data)}")
            return client_data
        
        # Create a Pydantic object for validation and serialization
        client = ClientOut(**client_data)
        logger.debug(f"TOOL get_client response: {client.model_dump()}")
        return {"success": True, "client": client.model_dump()}
    except Exception as e:
        # Catch any error and return it in the response
        logger.error(f"Unexpected error in get_client: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="create_client",
    description="Create a new client in the database",
)
async def create_client_tool(name: str, city: str = "", email: str = "") -> dict:
    """
    Create a new client in the database
    
    Args:
        name: Client's name
        city: Client's city (optional)
        email: Client's email (optional)
    """
    try:
        # Create a Pydantic model to validate input data
        client_in = ClientCreate(
            name=name, 
            city=city if city else None, 
            email=email if email else None
        )
        
        # Call the service to create the client in the database
        new_client_data = await service_create_client(client_in.name, client_in.city, client_in.email)
        
        if isinstance(new_client_data, dict) and not new_client_data.get("success", True):
            logger.error(f"Error creating client: {new_client_data.get('error', new_client_data)}")
            return new_client_data
        
        # Create a Pydantic object for validation and serialization of the response
        new_client = ClientOut(**new_client_data)
        logger.info(f"TOOL create_client response: {new_client.model_dump()}")
        return {"success": True, "client": new_client.model_dump()}
    except Exception as e:
        # Catch any error and return it in the response
        logger.error(f"Unexpected error in create_client_tool: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="update_client",
    description="Update data of an existing client",
)
async def update_client_tool(client_id: int, name: str = "", city: str = "", email: str = "") -> dict:
    """
    Update data of an existing client
    """
    try:
        # Create the Pydantic model only with non-empty fields
        update_fields = {k: v for k, v in {"name": name, "city": city, "email": email}.items() if v}
        if not update_fields:
            logger.warning("No data provided to update in update_client_tool")
            return {"success": False, "error": "No data provided to update"}
        client_update_data = ClientUpdate(**update_fields)
        # Call the service with the model, not with kwargs
        updated_client_data = await service_update_client(client_id, client_update_data)
        if not updated_client_data:
            logger.warning(f"Client with ID {client_id} not found or error updating")
            return {"success": False, "error": f"Client with ID {client_id} not found or error updating"}
        if isinstance(updated_client_data, dict) and not updated_client_data.get("success", True):
            logger.error(f"Error updating client: {updated_client_data.get('error', updated_client_data)}")
            return updated_client_data
        updated_client = ClientOut(**updated_client_data)
        logger.info(f"TOOL update_client response: {updated_client.model_dump()}")
        return {"success": True, "client": updated_client.model_dump()}
    except Exception as e:
        logger.error(f"Unexpected error in update_client_tool: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="delete_client",
    description="Delete a client from the database",
)
async def delete_client_tool(client_id: int) -> ClientDeleteResponse:
    """
    Delete a client from the database
    
    Args:
        client_id: ID of the client to delete
    """
    try:
        # First check that the client exists
        client_to_delete_data = await service_get_client_by_id(client_id)
        if not client_to_delete_data:
            # If the client is not found, return an error message
            logger.warning(f"Client with ID {client_id} not found for deletion")
            return ClientDeleteResponse(success=False, message=f"Client with ID {client_id} not found")
        
        if isinstance(client_to_delete_data, dict) and not client_to_delete_data.get("success", True):
            logger.error(f"Error getting client for deletion: {client_to_delete_data.get('error', client_to_delete_data)}")
            return ClientDeleteResponse(success=False, message=client_to_delete_data.get("error", "Unknown error"))
        
        # Create a Pydantic object for the client to be deleted
        deleted_client_out = ClientOut(**client_to_delete_data)
        
        # Call the service to delete the client from the database
        deleted = await service_delete_client(client_id)
        if deleted:
            # If successfully deleted, return a success message and the deleted client data
            logger.info(f"TOOL delete_client response: Client ID {client_id} deleted")
            return ClientDeleteResponse(
                success=True, 
                message=f"Client with ID {client_id} deleted successfully",
                deleted_client=deleted_client_out
            )
        else:
            # If there was a problem deleting, return an error message
            logger.error(f"Could not delete client with ID {client_id}")
            return ClientDeleteResponse(success=False, message=f"Could not delete client with ID {client_id}")
    except Exception as e:
        # Catch any error and return it in the response
        logger.error(f"Unexpected error in delete_client_tool: {e}")
        return ClientDeleteResponse(success=False, message=str(e))
