"""
Repositorio para acceso a datos de clientes (patrón Repository).
Centraliza la lógica de acceso a la base de datos para clientes.
"""

from typing import Optional, Dict, Any
import asyncpg
from backend.models.client import ClientCreate, ClientUpdate


class ClientRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, name, email, phone, city, created_at, updated_at
                FROM clients
                WHERE id = $1
                """,
                client_id,
            )
            return dict(row) if row else None

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, name, email, phone, city, created_at, updated_at
                FROM clients
                WHERE email = $1
                """,
                email.lower(),
            )
            return dict(row) if row else None

    async def create(self, client: ClientCreate) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO clients (name, email, phone, city)
                VALUES ($1, $2, $3, $4)
                RETURNING id, name, email, phone, city, created_at, updated_at
                """,
                client.name,
                client.email.lower(),
                client.phone,
                client.city,
            )
            return dict(row)

    async def update(
        self, client_id: int, update_data: ClientUpdate
    ) -> Optional[Dict[str, Any]]:
        fields = []
        values = []
        if update_data.name is not None:
            fields.append("name = $%d" % (len(values) + 1))
            values.append(update_data.name)
        if update_data.email is not None:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT id FROM clients WHERE email = $1 AND id != $2",
                    update_data.email.lower(),
                    client_id,
                )
                if row:
                    raise ValueError("El email ya está registrado por otro cliente.")
            fields.append("email = $%d" % (len(values) + 1))
            values.append(update_data.email.lower())
        if update_data.phone is not None:
            fields.append("phone = $%d" % (len(values) + 1))
            values.append(update_data.phone)
        if update_data.city is not None:
            fields.append("city = $%d" % (len(values) + 1))
            values.append(update_data.city)
        if not fields:
            return await self.get_by_id(client_id)
        fields.append("updated_at = CURRENT_TIMESTAMP")
        set_clause = ", ".join(fields)
        values.append(client_id)
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                f"""
                UPDATE clients SET {set_clause}
                WHERE id = ${len(values)}
                RETURNING id, name, email, phone, city, created_at, updated_at
                """,
                *values,
            )
            return dict(row) if row else None

    async def delete(self, client_id: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute("DELETE FROM clients WHERE id = $1", client_id)
            return result and result.startswith("DELETE")

    async def list_clients(
        self,
        name: Optional[str] = None,
        city: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Dict[str, Any]]:
        """
        Lista clientes con opción de filtrar por nombre y ciudad, y paginación.
        Args:
            name: filtro por nombre (opcional, búsqueda parcial, case-insensitive)
            city: filtro por ciudad (opcional, búsqueda parcial, case-insensitive)
            limit: máximo de resultados a devolver
            offset: desplazamiento para paginación
        Returns:
            Lista de diccionarios con los datos de los clientes
        """
        filters = []
        values = []
        if name:
            filters.append("LOWER(name) LIKE $%d" % (len(values) + 1))
            values.append(f"%{name.lower()}%")
        if city:
            filters.append("LOWER(city) LIKE $%d" % (len(values) + 1))
            values.append(f"%{city.lower()}%")
        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""
        values.extend([limit, offset])
        query = f"""
            SELECT id, name, email, phone, city, created_at, updated_at
            FROM clients
            {where_clause}
            ORDER BY id
            LIMIT $%d OFFSET $%d
        """ % (len(values) - 1, len(values))
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *values)
            return [dict(row) for row in rows]
