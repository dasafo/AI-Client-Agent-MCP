from backend.core.database import database
from backend.models.manager import ManagerOut
from typing import List, Optional, Dict, Any
from backend.core.logging import get_logger

# Logger for the manager service
logger = get_logger(__name__)

# Service to query authorized managers

async def get_manager_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves an authorized manager by their name.

    Args:
        name: Name of the manager to search for.
    Returns:
        Dictionary with manager data or None if not found.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers WHERE name = $1"
        row = await database.fetchrow(query, name)
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error in get_manager_by_name: {e}")
        return None

async def get_manager_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves an authorized manager by their email.

    Args:
        email: Email of the manager to search for.
    Returns:
        Dictionary with manager data or None if not found.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers WHERE email = $1"
        row = await database.fetchrow(query, email)
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error in get_manager_by_email: {e}")
        return None

async def list_managers() -> List[Dict[str, Any]]:
    """
    Lists all authorized managers.

    Returns:
        List of dictionaries with manager data.
    """
    try:
        query = "SELECT id, name, email, role, created_at FROM managers ORDER BY id"
        rows = await database.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error in list_managers: {e}")
        return []
