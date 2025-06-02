# backend/services/client_service.py
from backend.core.database import database
from backend.core.decorators import with_db_connection, db_transaction
from typing import List, Dict, Any, Optional
from backend.core.logging import get_logger

# Client management services
# These functions implement business logic and database access for clients

logger = get_logger(__name__)

@with_db_connection
async def get_all_clients(conn=None) -> List[Dict[str, Any]]:
    """
    Obtiene todos los clientes ordenados por ID.

    Args:
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Lista de diccionarios con los datos de los clientes.
    """
    try:
        rows = await conn.fetch(
            "SELECT id, name, city, email, created_at FROM clients ORDER BY id"
        )
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Error en get_all_clients: {e}")
        return []

@with_db_connection
async def get_client_by_id(client_id: int, conn=None) -> Optional[Dict[str, Any]]:
    """
    Obtiene un cliente específico por su ID.

    Args:
        client_id: ID del cliente a buscar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos del cliente o None si no se encuentra.
    """
    try:
        row = await conn.fetchrow(
            "SELECT id, name, city, email, created_at FROM clients WHERE id = $1",
            client_id
        )
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error en get_client_by_id: {e}")
        return None

@with_db_connection
async def create_client(name: str, city: str = "", email: str = "", conn=None) -> Dict[str, Any]:
    """
    Crea un nuevo cliente en la base de datos.

    Args:
        name: Nombre del cliente (obligatorio).
        city: Ciudad del cliente (opcional).
        email: Email del cliente (opcional).
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos del cliente creado.
    """
    try:
        query = """
            INSERT INTO clients (name, city, email) 
            VALUES ($1, $2, $3) 
            RETURNING id, name, city, email, created_at
        """
        row = await conn.fetchrow(query, name, city, email)
        return dict(row)
    except Exception as e:
        logger.error(f"Error en create_client: {e}")
        return {"success": False, "error": str(e)}

@with_db_connection
async def update_client(client_id: int, client_data: 'ClientUpdate', conn=None) -> Optional[Dict[str, Any]]:
    """
    Actualiza los datos de un cliente existente usando una consulta dinámica y exclude_unset.

    Args:
        client_id: ID del cliente a actualizar.
        client_data: Modelo ClientUpdate con los campos a actualizar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos del cliente actualizado o None si no se encuentra.
    """
    try:
        current_client = await get_client_by_id(client_id, conn=conn)
        if not current_client:
            logger.info(f"Cliente con ID {client_id} no encontrado para actualizar")
            return None
        update_fields = client_data.model_dump(exclude_unset=True)
        if not update_fields:
            logger.info(f"No hay campos para actualizar en el cliente ID {client_id}")
            return current_client
        set_clauses = []
        values = []
        for idx, (key, value) in enumerate(update_fields.items(), start=1):
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
        values.append(client_id)
        set_clause_str = ', '.join(set_clauses)
        id_placeholder = f"${len(values)}"
        query = f"""
            UPDATE clients 
            SET {set_clause_str} 
            WHERE id = {id_placeholder}
            RETURNING id, name, city, email, created_at
        """
        row = await conn.fetchrow(query, *values)
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error en update_client: {e}")
        return None

@with_db_connection
async def delete_client(client_id: int, conn=None) -> bool:
    """
    Elimina un cliente de la base de datos.

    Args:
        client_id: ID del cliente a eliminar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Booleano que indica si la eliminación fue exitosa.
    """
    try:
        client = await get_client_by_id(client_id, conn=conn)
        if not client:
            logger.info(f"Cliente con ID {client_id} no encontrado para eliminar")
            return False
        query = "DELETE FROM clients WHERE id = $1"
        result = await conn.execute(query, client_id)
        return "DELETE" in result
    except Exception as e:
        logger.error(f"Error en delete_client: {e}")
        return False

# Example of a function that uses a transaction
@db_transaction
async def transfer_client_data(source_client_id: int, target_client_id: int, conn=None) -> bool:
    """
    Transfiere datos de un cliente a otro dentro de una transacción.
    Ambos clientes deben existir.

    Args:
        source_client_id: ID del cliente origen.
        target_client_id: ID del cliente destino.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Booleano que indica si la transferencia fue exitosa.
    """
    try:
        source_client = await conn.fetchrow(
            "SELECT name, city, email FROM clients WHERE id = $1",
            source_client_id
        )
        if not source_client:
            logger.warning(f"Cliente origen con ID {source_client_id} no encontrado")
            return False
        target_client = await conn.fetchrow(
            "SELECT id FROM clients WHERE id = $1",
            target_client_id
        )
        if not target_client:
            logger.warning(f"Cliente destino con ID {target_client_id} no encontrado")
            return False
        await conn.execute(
            "UPDATE invoices SET client_id = $1 WHERE client_id = $2",
            target_client_id, source_client_id
        )
        await conn.execute(
            "DELETE FROM clients WHERE id = $1",
            source_client_id
        )
        logger.info(f"Transferencia de datos de cliente {source_client_id} a {target_client_id} realizada con éxito")
        return True
    except Exception as e:
        logger.error(f"Error en transfer_client_data: {e}")
        return False
