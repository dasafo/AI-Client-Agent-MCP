from backend.core.database import database
from backend.models.manager import ManagerOut
from typing import List, Optional, Dict, Any

# Servicio para consultar managers autorizados

async def get_manager_by_name(name: str) -> Optional[Dict[str, Any]]:
    query = "SELECT id, name, email, role, created_at FROM managers WHERE name = $1"
    row = await database.fetchrow(query, name)
    return row

async def get_manager_by_email(email: str) -> Optional[Dict[str, Any]]:
    query = "SELECT id, name, email, role, created_at FROM managers WHERE email = $1"
    row = await database.fetchrow(query, email)
    return row

async def list_managers() -> List[Dict[str, Any]]:
    query = "SELECT id, name, email, role, created_at FROM managers ORDER BY id"
    rows = await database.fetch(query)
    return rows
