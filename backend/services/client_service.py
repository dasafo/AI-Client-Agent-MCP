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
    Get all clients ordered by ID.
    
    Args:
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        List of dictionaries containing client data.
    """
    rows = await conn.fetch(
        "SELECT id, name, city, email, created_at FROM clients ORDER BY id"
    )
    return [dict(row) for row in rows]

@with_db_connection
async def get_client_by_id(client_id: int, conn=None) -> Optional[Dict[str, Any]]:
    """
    Get a specific client by ID.
    
    Args:
        client_id: ID of the client to find.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with client data or None if not found.
    """
    row = await conn.fetchrow(
        "SELECT id, name, city, email, created_at FROM clients WHERE id = $1",
        client_id
    )
    return dict(row) if row else None

@with_db_connection
async def create_client(name: str, city: str = "", email: str = "", conn=None) -> Dict[str, Any]:
    """
    Create a new client in the database.
    
    Args:
        name: Client name (required).
        city: Client city (optional).
        email: Client email (optional).
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with the created client data.
    """
    query = """
        INSERT INTO clients (name, city, email) 
        VALUES ($1, $2, $3) 
        RETURNING id, name, city, email, created_at
    """
    
    row = await conn.fetchrow(query, name, city, email)
    return dict(row)

@with_db_connection
async def update_client(client_id: int, client_data: 'ClientUpdate', conn=None) -> Optional[Dict[str, Any]]:
    """
    Update an existing client's data using a dynamic query and exclude_unset, similar to update_invoice.
    
    Args:
        client_id: ID of the client to update.
        client_data: ClientUpdate model with fields to update.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with updated client data or None if not found.
    """
    # First verify the client exists
    current_client = await get_client_by_id(client_id, conn=conn)
    if not current_client:
        logger.info(f"Client with ID {client_id} not found for update")
        return None
    
    # Get fields to update (only those that were set)
    update_fields = client_data.model_dump(exclude_unset=True)
    if not update_fields:
        logger.info(f"No fields to update for client ID {client_id}")
        return current_client
    
    # Build dynamic query based on provided fields
    set_clauses = []
    values = []
    for idx, (key, value) in enumerate(update_fields.items(), start=1):
        set_clauses.append(f"{key} = ${idx}")
        values.append(value)
    # Add client ID as the last parameter
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

@with_db_connection
async def delete_client(client_id: int, conn=None) -> bool:
    """
    Delete a client from the database.
    
    Args:
        client_id: ID of the client to delete.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Boolean indicating if deletion was successful.
    """
    # First check if the client exists
    client = await get_client_by_id(client_id, conn=conn)
    if not client:
        logger.info(f"Client with ID {client_id} not found for deletion")
        return False
    
    query = "DELETE FROM clients WHERE id = $1"
    
    result = await conn.execute(query, client_id)
    # Parse the DELETE result to determine success
    return "DELETE" in result

# Example of a function that uses a transaction
@db_transaction
async def transfer_client_data(source_client_id: int, target_client_id: int, conn=None) -> bool:
    """
    Transfer data from one client to another within a transaction.
    Both source and target client must exist.
    
    Args:
        source_client_id: ID of the source client.
        target_client_id: ID of the target client.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Boolean indicating if the transfer was successful.
    """
    # Get source client
    source_client = await conn.fetchrow(
        "SELECT name, city, email FROM clients WHERE id = $1",
        source_client_id
    )
    
    if not source_client:
        logger.warning(f"Source client with ID {source_client_id} not found")
        return False
    
    # Get target client
    target_client = await conn.fetchrow(
        "SELECT id FROM clients WHERE id = $1",
        target_client_id
    )
    
    if not target_client:
        logger.warning(f"Target client with ID {target_client_id} not found")
        return False
    
    # Update invoices to point to target client
    await conn.execute(
        "UPDATE invoices SET client_id = $1 WHERE client_id = $2",
        target_client_id, source_client_id
    )
    
    # Delete source client
    await conn.execute(
        "DELETE FROM clients WHERE id = $1",
        source_client_id
    )
    
    logger.info(f"Successfully transferred data from client {source_client_id} to {target_client_id}")
    return True
