"""
Repositorio para acceso a datos de notas de cliente.
"""

from typing import Optional, Dict, Any, List
import asyncpg
from backend.models.client_note import ClientNoteCreate


class ClientNoteRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def add_note(self, note: ClientNoteCreate) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO client_notes (client_id, note)
                VALUES ($1, $2)
                RETURNING id, client_id, note, created_at
                """,
                note.client_id,
                note.note,
            )
            return dict(row)

    async def list_notes(self, client_id: int) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id, client_id, note, created_at
                FROM client_notes
                WHERE client_id = $1
                ORDER BY created_at DESC
                """,
                client_id,
            )
            return [dict(row) for row in rows]
