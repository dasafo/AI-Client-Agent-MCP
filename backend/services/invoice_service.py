from backend.core.database import database
from backend.core.decorators import with_db_connection, db_transaction
from backend.models.invoice import InvoiceCreate, InvoiceUpdate
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date
import asyncpg
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Invoice management services
# These functions implement business logic and database access for invoices
# All functions accept an optional connection to facilitate transactions and testing

@with_db_connection
async def get_all_invoices(conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Get all invoices ordered by ID.
    
    Args:
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        List of dictionaries containing invoice data.
    """
    query = """
        SELECT id, client_id, amount, issued_at, due_date, status
        FROM invoices
        ORDER BY id
    """
    
    rows = await conn.fetch(query)
    return [dict(row) for row in rows]

@with_db_connection
async def get_invoice_by_id(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Get a specific invoice by ID.
    
    Args:
        invoice_id: ID of the invoice to find.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with invoice data or None if not found.
    """
    query = """
        SELECT id, client_id, amount, issued_at, due_date, status
        FROM invoices
        WHERE id = $1
    """
    
    row = await conn.fetchrow(query, invoice_id)
    return dict(row) if row else None

@with_db_connection
async def get_invoices_by_client_id(client_id: int, conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Get all invoices for a specific client.
    
    Args:
        client_id: ID of the client whose invoices to retrieve.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        List of dictionaries containing invoice data for the client.
    """
    query = """
        SELECT id, client_id, amount, issued_at, due_date, status
        FROM invoices
        WHERE client_id = $1
        ORDER BY id
    """
    
    rows = await conn.fetch(query, client_id)
    return [dict(row) for row in rows]

@with_db_connection
async def create_invoice(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Create a new invoice in the database.
    
    Args:
        invoice_data: InvoiceCreate object with invoice data.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with the created invoice data.
        
    Raises:
        Exception: If invoice creation fails.
    """
    query = """
        INSERT INTO invoices (client_id, amount, issued_at, due_date, status) 
        VALUES ($1, $2, $3, $4, $5) 
        RETURNING id, client_id, amount, issued_at, due_date, status
    """
    
    # Default values if not provided in the model
    issued_at = invoice_data.issued_at if invoice_data.issued_at is not None else date.today()
    status = invoice_data.status if invoice_data.status is not None else 'pending'
    
    row = await conn.fetchrow(
        query,
        invoice_data.client_id, 
        invoice_data.amount,
        issued_at,
        invoice_data.due_date,
        status
    )
    
    if not row:
        logger.error("Failed to create invoice")
        raise Exception("Failed to create invoice")
    
    return dict(row)

@with_db_connection
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Update an existing invoice's data.
    
    Args:
        invoice_id: ID of the invoice to update.
        invoice_data: InvoiceUpdate object with fields to update.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with updated invoice data or None if not found.
    """
    # First verify the invoice exists
    current_invoice = await get_invoice_by_id(invoice_id, conn=conn)
    if not current_invoice:
        logger.info(f"Invoice with ID {invoice_id} not found for update")
        return None
    
    # Get fields to update (only those that were set)
    update_fields = invoice_data.model_dump(exclude_unset=True)
    if not update_fields:
        logger.info(f"No fields to update for invoice ID {invoice_id}")
        return current_invoice
    
    # Build dynamic query based on provided fields
    set_clauses = []
    values = []
    i = 1
    
    for key, value in update_fields.items():
        set_clauses.append(f"{key} = ${i}")
        values.append(value)
        i += 1
    
    # Add invoice ID as the last parameter
    values.append(invoice_id)
    
    query = f"""
        UPDATE invoices 
        SET {', '.join(set_clauses)} 
        WHERE id = ${{i}}
        RETURNING id, client_id, amount, issued_at, due_date, status
    """
    
    row = await conn.fetchrow(query, *values)
    return dict(row) if row else None

@with_db_connection
async def delete_invoice(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> bool:
    """
    Delete an invoice from the database.
    
    Args:
        invoice_id: ID of the invoice to delete.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Boolean indicating if deletion was successful.
    """
    # First check if the invoice exists
    invoice = await get_invoice_by_id(invoice_id, conn=conn)
    if not invoice:
        logger.info(f"Invoice with ID {invoice_id} not found for deletion")
        return False
    
    query = "DELETE FROM invoices WHERE id = $1"
    
    result = await conn.execute(query, invoice_id)
    return "DELETE" in result

@db_transaction
async def create_invoice_with_verification(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Create a new invoice with additional client verification within a transaction.
    
    Args:
        invoice_data: InvoiceCreate object with invoice data.
        conn: Optional database connection. If not provided, a new one is created.
        
    Returns:
        Dictionary with the created invoice data.
        
    Raises:
        Exception: If client doesn't exist or invoice creation fails.
    """
    # First verify that the client exists
    client = await conn.fetchrow(
        "SELECT id FROM clients WHERE id = $1",
        invoice_data.client_id
    )
    
    if not client:
        error_msg = f"Cannot create invoice: Client with ID {invoice_data.client_id} does not exist"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Create the invoice within the same transaction
    query = """
        INSERT INTO invoices (client_id, amount, issued_at, due_date, status) 
        VALUES ($1, $2, $3, $4, $5) 
        RETURNING id, client_id, amount, issued_at, due_date, status
    """
    
    # Default values if not provided in the model
    issued_at = invoice_data.issued_at if invoice_data.issued_at is not None else date.today()
    status = invoice_data.status if invoice_data.status is not None else 'pending'
    
    row = await conn.fetchrow(
        query,
        invoice_data.client_id, 
        invoice_data.amount,
        issued_at,
        invoice_data.due_date,
        status
    )
    
    if not row:
        logger.error("Failed to create invoice")
        raise Exception("Failed to create invoice")
    
    # Log the successful creation
    invoice_id = dict(row)["id"]
    logger.info(f"Successfully created invoice {invoice_id} for client {invoice_data.client_id}")
    
    return dict(row) 