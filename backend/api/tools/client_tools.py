"""
Módulo que contiene las herramientas (tools) relacionadas con clientes para la API MCP.
Estas herramientas exponen funcionalidades específicas que pueden ser llamadas a través de la API.
"""
import logging
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Context

# Configuración de logging
logger = logging.getLogger(__name__)

# Importaciones locales
from backend.services.client_service import ClientService

async def search_client_by_email(email: str, ctx: Context) -> Dict[str, Any]:
    """
    Busca un cliente por su dirección de correo electrónico.
    
    Args:
        email: Dirección de correo electrónico del cliente a buscar
        ctx: Contexto de la petición MCP
        
    Returns:
        dict: Datos del cliente encontrado o mensaje de error
        
    Raises:
        Exception: Si ocurre un error al buscar el cliente
    """
    try:
        pool = ctx.request_context.lifespan_context
        client_service = ClientService(pool)
        client = await client_service.get_client_by_email(email)
        
        if not client:
            return {"error": f"No se encontró cliente con email {email}"}
            
        return client
        
    except Exception as e:
        logger.error(f"Error al buscar cliente por email {email}: {str(e)}")
        return {"error": "Error al buscar el cliente"}

async def add_client(
    name: str, 
    email: str, 
    phone: str = None, 
    city: str = None, 
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Añade un nuevo cliente a la base de datos.
    
    Args:
        name: Nombre del cliente
        email: Correo electrónico del cliente
        phone: Número de teléfono (opcional)
        city: Ciudad de residencia (opcional)
        ctx: Contexto de la petición MCP
        
    Returns:
        dict: Confirmación de la operación o mensaje de error
        
    Raises:
        Exception: Si ocurre un error al crear el cliente
    """
    pool: asyncpg.Pool = ctx.request_context.lifespan_context
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO clients (name, email, phone, city) 
            VALUES ($1, $2, $3, $4)
            """,
            name, 
            email.lower(),  # Normalizamos el email a minúsculas
            phone, 
            city
        )
    return {
        "success": True, 
        "message": f"Cliente {name} añadido correctamente"
    }

def register_tools(mcp: FastMCP) -> None:
    """
    Registra las herramientas en la instancia de MCP.
    
    Args:
        mcp: Instancia de FastMCP donde se registrarán las herramientas
    """
    mcp.add_tool(
        search_client_by_email,
        name="search_client_by_email",
        description="Buscar un cliente por su dirección de correo electrónico"
    )
    mcp.add_tool(
        add_client,
        name="add_client",
        description="Añadir un nuevo cliente a la base de datos"
    )
