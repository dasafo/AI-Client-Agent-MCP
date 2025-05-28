from backend.mcp_instance import mcp
from backend.services.client_service import get_all_clients, create_client, update_client, get_client_by_id, delete_client
from typing import Optional


@mcp.tool(
    name="list_clients",
    description="Listar clientes de la base de datos",
)
async def list_clients():
    try:
        clients = await get_all_clients()  # Ya es lista de dicts
        print("TOOL list_clients responde:", clients)  # (opcional, para debug)
        return {"success": True, "clients": clients}
    except Exception as e:
        print("ERROR en list_clients:", str(e))  # (opcional, para debug)
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="get_client",
    description="Obtener un cliente por su ID",
)
async def get_client(client_id: int):
    """
    Obtener un cliente por su ID
    
    Args:
        client_id: ID del cliente a consultar
    """
    try:
        client = await get_client_by_id(client_id)
        if not client:
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
        
        print(f"TOOL get_client responde: {client}")  # (opcional, para debug)
        return {"success": True, "client": client}
    except Exception as e:
        print(f"ERROR en get_client: {str(e)}")  # (opcional, para debug)
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="create_client",
    description="Crear un nuevo cliente en la base de datos",
)
async def create_client_tool(name: str, city: str, email: str):
    """
    Crear un nuevo cliente en la base de datos
    
    Args:
        name: Nombre del cliente
        city: Ciudad del cliente
        email: Email del cliente
    """
    try:
        new_client = await create_client(name, city, email)
        print(f"TOOL create_client responde: {new_client}")  # (opcional, para debug)
        return {"success": True, "client": new_client}
    except Exception as e:
        print(f"ERROR en create_client: {str(e)}")  # (opcional, para debug)
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="update_client",
    description="Actualizar datos de un cliente existente",
)
async def update_client_tool(client_id: int, name: Optional[str] = None, city: Optional[str] = None, email: Optional[str] = None):
    """
    Actualizar datos de un cliente existente
    
    Args:
        client_id: ID del cliente a actualizar
        name: Nuevo nombre del cliente (opcional)
        city: Nueva ciudad del cliente (opcional)
        email: Nuevo email del cliente (opcional)
    """
    try:
        # Verificar que el cliente existe
        client = await get_client_by_id(client_id)
        if not client:
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
        
        # Actualizar cliente
        updated_client = await update_client(client_id, name, city, email)
        print(f"TOOL update_client responde: {updated_client}")  # (opcional, para debug)
        return {"success": True, "client": updated_client}
    except Exception as e:
        print(f"ERROR en update_client: {str(e)}")  # (opcional, para debug)
        return {"success": False, "error": str(e)}


@mcp.tool(
    name="delete_client",
    description="Eliminar un cliente de la base de datos",
)
async def delete_client_tool(client_id: int):
    """
    Eliminar un cliente de la base de datos
    
    Args:
        client_id: ID del cliente a eliminar
    """
    try:
        # Verificar que el cliente existe
        client = await get_client_by_id(client_id)
        if not client:
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
        
        # Guardar una copia de los datos del cliente antes de eliminarlo
        client_data = client.copy()
        
        # Eliminar el cliente
        deleted = await delete_client(client_id)
        if deleted:
            print(f"TOOL delete_client responde: Cliente ID {client_id} eliminado")  # (opcional, para debug)
            return {
                "success": True, 
                "message": f"Cliente con ID {client_id} eliminado correctamente",
                "deleted_client": client_data
            }
        else:
            return {"success": False, "error": f"No se pudo eliminar el cliente con ID {client_id}"}
    except Exception as e:
        print(f"ERROR en delete_client: {str(e)}")  # (opcional, para debug)
        return {"success": False, "error": str(e)}
