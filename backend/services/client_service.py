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

async def get_client_by_id(client_id):
    pool = await database.connect()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, name, city, email, created_at FROM clients WHERE id = $1",
            client_id
        )
        return dict(row) if row else None

async def create_client(name, city, email):
    pool = await database.connect()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO clients (name, city, email) 
            VALUES ($1, $2, $3) 
            RETURNING id, name, city, email, created_at
            """,
            name, city, email
        )
        return dict(row)

async def update_client(client_id, name=None, city=None, email=None):
    # Primero obtenemos el cliente actual
    client = await get_client_by_id(client_id)
    if not client:
        return None
        
    # Actualizamos solo los campos proporcionados
    name = name if name is not None else client['name']
    city = city if city is not None else client['city']
    email = email if email is not None else client['email']
    
    pool = await database.connect()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE clients 
            SET name = $1, city = $2, email = $3 
            WHERE id = $4
            RETURNING id, name, city, email, created_at
            """,
            name, city, email, client_id
        )
        return dict(row) if row else None

async def delete_client(client_id):
    # Primero verificamos que el cliente existe
    client = await get_client_by_id(client_id)
    if not client:
        return False
    
    pool = await database.connect()
    async with pool.acquire() as conn:
        # Eliminamos el cliente
        result = await conn.execute(
            "DELETE FROM clients WHERE id = $1",
            client_id
        )
        # Si la consulta afectó a una fila, significa que se eliminó correctamente
        return result == "DELETE 1"
