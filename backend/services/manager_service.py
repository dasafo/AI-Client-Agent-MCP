from backend.core.database import database
from backend.models.manager import ManagerOut
from typing import List, Optional, Dict, Any
from backend.core.logging import get_logger

# Logger para el servicio de managers
logger = get_logger(__name__)

# Servicio para consultar managers autorizados

async def get_manager_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene un manager autorizado por su nombre.

    Args:
        name: Nombre del manager a buscar.
    Returns:
        Diccionario con los datos del manager o None si no se encuentra.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers WHERE name = $1"
        row = await database.fetchrow(query, name)
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error en get_manager_by_name: {e}")
        return None

async def get_manager_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene un manager autorizado por su email.

    Args:
        email: Email del manager a buscar.
    Returns:
        Diccionario con los datos del manager o None si no se encuentra.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers WHERE email = $1"
        row = await database.fetchrow(query, email)
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error en get_manager_by_email: {e}")
        return None

async def list_managers() -> List[Dict[str, Any]]:
    """
    Lista todos los managers autorizados.

    Returns:
        Lista de diccionarios con los datos de los managers.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers ORDER BY id"
        rows = await database.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error en list_managers: {e}")
        return []
