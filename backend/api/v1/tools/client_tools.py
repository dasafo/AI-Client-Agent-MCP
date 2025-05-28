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


@mcp.tool(
    name="list_clients",
    description="Listar clientes de la base de datos",
)
async def list_clients() -> dict:
    """Listar clientes de la base de datos"""
    try:
        clients_data = await service_get_all_clients()
        processed_clients = []
        for client_dict in clients_data:
            if isinstance(client_dict.get('created_at'), datetime):
                client_dict['created_at'] = client_dict['created_at'].isoformat()
            processed_clients.append(ClientOut(**client_dict))
        return {"success": True, "clients": [c.model_dump() for c in processed_clients]}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="get_client",
    description="Obtener un cliente por su ID",
)
async def get_client(client_id: int) -> dict:
    """
    Obtener un cliente por su ID
    
    Args:
        client_id: ID del cliente a consultar
    """
    try:
        client_data = await service_get_client_by_id(client_id)
        if not client_data:
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
        
        if isinstance(client_data.get('created_at'), datetime):
            client_data['created_at'] = client_data['created_at'].isoformat()
            
        client = ClientOut(**client_data)
        return {"success": True, "client": client.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="create_client",
    description="Crear un nuevo cliente en la base de datos",
)
async def create_client_tool(name: str, city: str = "", email: str = "") -> dict:
    """
    Crear un nuevo cliente en la base de datos
    
    Args:
        name: Nombre del cliente
        city: Ciudad del cliente (opcional)
        email: Email del cliente (opcional)
    """
    try:
        client_in = ClientCreate(
            name=name, 
            city=city if city else None, 
            email=email if email else None
        )
        new_client_data = await service_create_client(client_in.name, client_in.city, client_in.email)
        
        if isinstance(new_client_data.get('created_at'), datetime):
            new_client_data['created_at'] = new_client_data['created_at'].isoformat()
            
        new_client = ClientOut(**new_client_data)
        return {"success": True, "client": new_client.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="update_client",
    description="Actualizar datos de un cliente existente",
)
async def update_client_tool(client_id: int, name: str = "", city: str = "", email: str = "") -> dict:
    """
    Actualizar datos de un cliente existente
    
    Args:
        client_id: ID del cliente a actualizar
        name: Nuevo nombre del cliente (opcional)
        city: Nueva ciudad del cliente (opcional)
        email: Nuevo email del cliente (opcional)
    """
    try:
        client_update_data = ClientUpdate(
            name=name if name else None, 
            city=city if city else None, 
            email=email if email else None
        )
        
        update_data_dict = client_update_data.model_dump(exclude_unset=True)
        if not update_data_dict:
            return {"success": False, "error": "No se proporcionaron datos para actualizar"}
            
        updated_client_data = await service_update_client(client_id, **update_data_dict)
        if not updated_client_data:
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado o error al actualizar"}
            
        if isinstance(updated_client_data.get('created_at'), datetime):
            updated_client_data['created_at'] = updated_client_data['created_at'].isoformat()

        updated_client = ClientOut(**updated_client_data)
        return {"success": True, "client": updated_client.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="delete_client",
    description="Eliminar un cliente de la base de datos",
)
async def delete_client_tool(client_id: int) -> ClientDeleteResponse:
    """
    Eliminar un cliente de la base de datos
    
    Args:
        client_id: ID del cliente a eliminar
    """
    try:
        client_to_delete_data = await service_get_client_by_id(client_id)
        if not client_to_delete_data:
            return ClientDeleteResponse(success=False, message=f"Cliente con ID {client_id} no encontrado")
        
        if isinstance(client_to_delete_data.get('created_at'), datetime):
            client_to_delete_data['created_at'] = client_to_delete_data['created_at'].isoformat()

        deleted_client_out = ClientOut(**client_to_delete_data)
        
        deleted = await service_delete_client(client_id)
        if deleted:
            return ClientDeleteResponse(
                success=True, 
                message=f"Cliente con ID {client_id} eliminado correctamente",
                deleted_client=deleted_client_out
            )
        else:
            return ClientDeleteResponse(success=False, message=f"No se pudo eliminar el cliente con ID {client_id}")
    except Exception as e:
        return ClientDeleteResponse(success=False, message=str(e))
