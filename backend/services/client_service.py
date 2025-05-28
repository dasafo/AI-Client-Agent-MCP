# backend/services/client_service.py
from backend.core.database import database


async def get_all_clients():
    pool = await database.connect()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, city, email, created_at FROM clients ORDER BY id"
        )
        # Devuelve lista de dicts
        return [dict(row) for row in rows]
