"""
Módulo de herramientas de cliente para la API MCP.
Estas herramientas exponen funcionalidades relacionadas con clientes que pueden ser llamadas a través de la API MCP.
"""

import logging
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP, Context
from backend.services.client_service import ClientService
from backend.models.client import ClientCreate, ClientUpdate
from backend.models.client_note import ClientNoteCreate
import asyncpg
import httpx
from .tools_registry import mcp_tool
from backend.core.database import database

# Configuración de logging
logger = logging.getLogger(__name__)


async def _get_pool_from_ctx(ctx: Optional[Context]) -> Any:
    """
    Obtiene el pool de conexiones desde el contexto MCP o, si no hay contexto, del pool global.
    Inicializa el pool global si es necesario.
    """
    if ctx is not None and getattr(ctx, "request_context", None) is not None:
        return ctx.request_context.lifespan_context
    # FastAPI puro: usar pool global
    if database._pool is None:
        await database.connect()
    return database._pool


@mcp_tool(
    name="search_client_by_email",
    description="Buscar un cliente por dirección de correo electrónico",
)
async def search_client_by_email(email: str, ctx: Context) -> Dict[str, Any]:
    """
    Buscar un cliente por dirección de correo electrónico usando el servicio.
    Devuelve un diccionario con los datos del cliente o un mensaje de error si no se encuentra.
    """
    try:
        pool = await _get_pool_from_ctx(ctx)
        if pool is None:
            return {"error": "No hay pool de base de datos disponible"}
        client_service = ClientService(pool)
        client = await client_service.get_client_by_email(email)
        if not client:
            return {"error": f"No se encontró cliente con el email {email}"}
        return client
    except Exception as e:
        logger.error(f"Error buscando cliente por email {email}: {str(e)}")
        return {"error": "Error al buscar el cliente"}


@mcp_tool(name="add_client", description="Añadir un nuevo cliente a la base de datos")
async def add_client(
    name: str,
    email: str,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Añadir un nuevo cliente a la base de datos usando el servicio.
    Realiza validación de unicidad y formato antes de crear el cliente.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"success": False, "error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    # Normaliza el email a minúsculas
    email = email.lower()
    # Comprobación de unicidad del email
    existing = await client_service.get_client_by_email(email)
    if existing:
        return {"success": False, "error": f"El email {email} ya está registrado"}
    # Se crea el objeto cliente y se almacena en la base de datos
    client_obj = ClientCreate(name=name, email=email, phone=phone, city=city)
    try:
        created = await client_service.create_client(client_obj)
        return {"success": True, "client": created}
    except asyncpg.UniqueViolationError:
        return {
            "success": False,
            "error": f"El email {email} ya está registrado (violación de restricción única)",
        }
    except Exception as e:
        logger.error(f"Error creando cliente: {str(e)}")
        return {"success": False, "error": "Error al crear el cliente"}


@mcp_tool(name="update_client", description="Actualizar un cliente existente por su ID")
async def update_client(
    client_id: int,
    update: dict,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Actualiza un cliente existente por su ID.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    try:
        update_data = ClientUpdate(**update)
        updated = await client_service.update_client(client_id, update_data)
        if not updated:
            return {"error": f"No se encontró cliente con id {client_id}"}
        return {"success": True, "client": updated}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        logger.error(f"Error actualizando cliente {client_id}: {str(e)}")
        return {"error": "Error al actualizar el cliente"}


@mcp_tool(name="delete_client", description="Eliminar un cliente por su ID")
async def delete_client(
    client_id: int,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Elimina un cliente por su ID.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    try:
        deleted = await client_service.delete_client(client_id)
        if not deleted:
            return {"error": f"No se encontró cliente con id {client_id}"}
        return {"success": True}
    except Exception as e:
        logger.error(f"Error eliminando cliente {client_id}: {str(e)}")
        return {"error": "Error al eliminar el cliente"}


@mcp_tool(
    name="list_clients",
    description="Listar clientes con filtros opcionales y paginación",
)
async def list_clients(
    name: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Devuelve una lista de clientes, con filtros opcionales por nombre y ciudad, y paginación.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"success": False, "error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    try:
        results = await client_service.list_clients(
            name=name, city=city, limit=limit, offset=offset
        )
        return {"success": True, "clients": results}
    except Exception as e:
        logger.error(f"Error listando clientes: {str(e)}")
        return {"success": False, "error": "Error al listar clientes"}


@mcp_tool(name="add_client_note", description="Añadir una nota a un cliente")
async def add_client_note(
    client_id: int,
    note: str,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Añade una nota a un cliente.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"success": False, "error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    try:
        note_obj = ClientNoteCreate(client_id=client_id, note=note)
        created = await client_service.add_note(note_obj)
        return {"success": True, "note": created}
    except Exception as e:
        logger.error(f"Error añadiendo nota a cliente {client_id}: {str(e)}")
        return {"success": False, "error": "Error al añadir la nota"}


@mcp_tool(name="list_client_notes", description="Listar notas de un cliente")
async def list_client_notes(
    client_id: int,
    ctx: Optional[Context] = None,
) -> Dict[str, Any]:
    """
    Lista todas las notas de un cliente.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"success": False, "error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    try:
        notes = await client_service.list_notes(client_id)
        return {"success": True, "notes": notes}
    except Exception as e:
        logger.error(f"Error listando notas de cliente {client_id}: {str(e)}")
        return {"success": False, "error": "Error al listar las notas"}


@mcp_tool(
    name="send_welcome_email",
    description="Enviar un email de bienvenida a un cliente usando un servidor MCP de emails externo.",
)
async def send_welcome_email(
    email: str,
    name: str,
    ctx: Optional[Context] = None,
    email_server_url: str = "http://localhost:8080/tools/send_email",
) -> Dict[str, Any]:
    """
    Envía un email de bienvenida a un cliente usando un servidor MCP de emails externo.
    Parámetros:
        email: Email del cliente
        name: Nombre del cliente
        email_server_url: URL del endpoint MCP de emails (por defecto: http://localhost:8080/tools/send_email)
    """
    subject = f"¡Bienvenido/a, {name}!"
    body = f"Hola {name},\n\nGracias por registrarte como cliente. ¡Bienvenido/a!\n\nSaludos,\nEl equipo."
    payload = {"to": email, "subject": subject, "body": body}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(email_server_url, json=payload, timeout=10)
            if response.status_code == 200:
                return {"success": True, "detail": "Email enviado correctamente"}
            else:
                return {
                    "success": False,
                    "error": f"Error del servidor de emails: {response.text}",
                }
    except Exception as e:
        logger.error(f"Error enviando email de bienvenida: {str(e)}")
        return {"success": False, "error": str(e)}


@mcp_tool(
    name="add_client_and_send_welcome_email",
    description="Añadir un cliente y enviarle un email de bienvenida usando un servidor MCP externo de emails.",
)
async def add_client_and_send_welcome_email(
    name: str,
    email: str,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    ctx: Optional[Context] = None,
    email_server_url: str = "http://localhost:8080/tools/send_email",
) -> Dict[str, Any]:
    """
    Añade un nuevo cliente y le envía un email de bienvenida usando un servidor MCP externo de emails.
    """
    pool = await _get_pool_from_ctx(ctx)
    if pool is None:
        return {"success": False, "error": "No hay pool de base de datos disponible"}
    client_service = ClientService(pool)
    email = email.lower()
    existing = await client_service.get_client_by_email(email)
    if existing:
        return {"success": False, "error": f"El email {email} ya está registrado"}
    client_obj = ClientCreate(name=name, email=email, phone=phone, city=city)
    try:
        created = await client_service.create_client(client_obj)
        subject = f"¡Bienvenido/a, {name}!"
        body = f"Hola {name},\n\nGracias por registrarte como cliente. ¡Bienvenido/a!\n\nSaludos,\nEl equipo."
        payload = {"to": email, "subject": subject, "body": body}
        async with httpx.AsyncClient() as client:
            response = await client.post(email_server_url, json=payload, timeout=10)
            email_result = response.status_code == 200
            email_detail = response.text
        return {
            "success": True,
            "client": created,
            "email_sent": email_result,
            "email_response": email_detail,
        }
    except asyncpg.UniqueViolationError:
        return {
            "success": False,
            "error": f"El email {email} ya está registrado (violación de restricción única)",
        }
    except Exception as e:
        logger.error(f"Error creando cliente o enviando email: {str(e)}")
        return {
            "success": False,
            "error": "Error al crear el cliente o enviar el email",
        }


def register_tools(mcp: FastMCP) -> None:
    """
    Registrar automáticamente las tools decoradas en la instancia MCP.
    """
    from .tools_registry import TOOLS

    for func, name, desc in TOOLS:
        mcp.add_tool(func, name=name, description=desc)
