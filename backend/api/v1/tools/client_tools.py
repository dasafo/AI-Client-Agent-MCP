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

# Herramientas para la gestión de clientes
# Estas funciones exponen la funcionalidad de gestión de clientes a través del MCP (Master Control Program)

@mcp.tool(
    name="list_clients",
    description="Listar clientes de la base de datos",
)
async def list_clients() -> dict:
    """Listar clientes de la base de datos"""
    try:
        # Obtiene todos los clientes desde el servicio
        clients_data = await service_get_all_clients()
        if isinstance(clients_data, dict) and not clients_data.get("success", True):
            logger.error(f"Error al listar clientes: {clients_data.get('error', clients_data)}")
            return clients_data
        processed_clients = []
        
        # Procesa cada cliente para manejar correctamente las fechas
        for client_dict in clients_data:
            processed_clients.append(ClientOut(**client_dict))
            
        # Devuelve la lista de clientes serializada
        logger.debug(f"TOOL list_clients responde: {[c.model_dump() for c in processed_clients]}")
        return {"success": True, "clients": [c.model_dump() for c in processed_clients]}
    except Exception as e:
        # Captura cualquier error y lo devuelve en la respuesta
        logger.error(f"Error inesperado en list_clients: {e}")
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
        # Busca el cliente por su ID utilizando el servicio
        client_data = await service_get_client_by_id(client_id)
        if not client_data:
            # Si no se encuentra el cliente, devuelve un mensaje de error
            logger.warning(f"Cliente con ID {client_id} no encontrado")
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
        
        if isinstance(client_data, dict) and not client_data.get("success", True):
            logger.error(f"Error al obtener cliente: {client_data.get('error', client_data)}")
            return client_data
        
        # Crea un objeto Pydantic para validación y serialización
        client = ClientOut(**client_data)
        logger.debug(f"TOOL get_client responde: {client.model_dump()}")
        return {"success": True, "client": client.model_dump()}
    except Exception as e:
        # Captura cualquier error y lo devuelve en la respuesta
        logger.error(f"Error inesperado en get_client: {e}")
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
        # Crea un modelo Pydantic para validar los datos de entrada
        client_in = ClientCreate(
            name=name, 
            city=city if city else None, 
            email=email if email else None
        )
        
        # Llama al servicio para crear el cliente en la base de datos
        new_client_data = await service_create_client(client_in.name, client_in.city, client_in.email)
        
        if isinstance(new_client_data, dict) and not new_client_data.get("success", True):
            logger.error(f"Error al crear cliente: {new_client_data.get('error', new_client_data)}")
            return new_client_data
        
        # Crea un objeto Pydantic para validación y serialización de la respuesta
        new_client = ClientOut(**new_client_data)
        logger.info(f"TOOL create_client responde: {new_client.model_dump()}")
        return {"success": True, "client": new_client.model_dump()}
    except Exception as e:
        # Captura cualquier error y lo devuelve en la respuesta
        logger.error(f"Error inesperado en create_client_tool: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="update_client",
    description="Actualizar datos de un cliente existente",
)
async def update_client_tool(client_id: int, name: str = "", city: str = "", email: str = "") -> dict:
    """
    Actualizar datos de un cliente existente
    """
    try:
        # Crea el modelo Pydantic solo con los campos no vacíos
        update_fields = {k: v for k, v in {"name": name, "city": city, "email": email}.items() if v}
        if not update_fields:
            logger.warning("No se proporcionaron datos para actualizar en update_client_tool")
            return {"success": False, "error": "No se proporcionaron datos para actualizar"}
        client_update_data = ClientUpdate(**update_fields)
        # Llama al servicio con el modelo, no con kwargs
        updated_client_data = await service_update_client(client_id, client_update_data)
        if not updated_client_data:
            logger.warning(f"Cliente con ID {client_id} no encontrado o error al actualizar")
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado o error al actualizar"}
        if isinstance(updated_client_data, dict) and not updated_client_data.get("success", True):
            logger.error(f"Error al actualizar cliente: {updated_client_data.get('error', updated_client_data)}")
            return updated_client_data
        updated_client = ClientOut(**updated_client_data)
        logger.info(f"TOOL update_client responde: {updated_client.model_dump()}")
        return {"success": True, "client": updated_client.model_dump()}
    except Exception as e:
        logger.error(f"Error inesperado en update_client_tool: {e}")
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
        # Primero verifica que el cliente exista
        client_to_delete_data = await service_get_client_by_id(client_id)
        if not client_to_delete_data:
            # Si no se encuentra el cliente, devuelve un mensaje de error
            logger.warning(f"Cliente con ID {client_id} no encontrado para eliminar")
            return ClientDeleteResponse(success=False, message=f"Cliente con ID {client_id} no encontrado")
        
        if isinstance(client_to_delete_data, dict) and not client_to_delete_data.get("success", True):
            logger.error(f"Error al obtener cliente para eliminar: {client_to_delete_data.get('error', client_to_delete_data)}")
            return ClientDeleteResponse(success=False, message=client_to_delete_data.get("error", "Error desconocido"))
        
        # Crea un objeto Pydantic para el cliente que se va a eliminar
        deleted_client_out = ClientOut(**client_to_delete_data)
        
        # Llama al servicio para eliminar el cliente de la base de datos
        deleted = await service_delete_client(client_id)
        if deleted:
            # Si se eliminó correctamente, devuelve un mensaje de éxito y los datos del cliente eliminado
            logger.info(f"TOOL delete_client responde: Cliente ID {client_id} eliminado")
            return ClientDeleteResponse(
                success=True, 
                message=f"Cliente con ID {client_id} eliminado correctamente",
                deleted_client=deleted_client_out
            )
        else:
            # Si hubo un problema al eliminar, devuelve un mensaje de error
            logger.error(f"No se pudo eliminar el cliente con ID {client_id}")
            return ClientDeleteResponse(success=False, message=f"No se pudo eliminar el cliente con ID {client_id}")
    except Exception as e:
        # Captura cualquier error y lo devuelve en la respuesta
        logger.error(f"Error inesperado en delete_client_tool: {e}")
        return ClientDeleteResponse(success=False, message=str(e))
