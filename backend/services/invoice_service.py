from backend.core.database import database
from backend.core.decorators import with_db_connection, db_transaction
from backend.models.invoice import InvoiceCreate, InvoiceUpdate
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date
import asyncpg
from backend.core.logging import get_logger
from backend.services.client_service import get_client_by_id

# Invoice management services
# These functions implement business logic and database access for invoices
# All functions accept an optional connection to facilitate transactions and testing

logger = get_logger(__name__)

@with_db_connection
async def get_all_invoices(conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Retrieves all invoices ordered by ID.

    Args:
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        List of dictionaries with invoice data.
    """
    try:
        query = """
            SELECT id, client_id, amount, issued_at, due_date, status
            FROM invoices
            ORDER BY id
        """
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_all_invoices: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_all_invoices: {e}")
        return []

@with_db_connection
async def get_invoice_by_id(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves a specific invoice by its ID.

    Args:
        invoice_id: ID of the invoice to search for.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        Dictionary with invoice data or None if not found.
    """
    try:
        query = """
            SELECT id, client_id, amount, issued_at, due_date, status
            FROM invoices
            WHERE id = $1
        """
        row = await conn.fetchrow(query, invoice_id)
        return dict(row) if row else None
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_invoice_by_id: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_invoice_by_id: {e}")
        return None

@with_db_connection
async def get_invoices_by_client_id(client_id: int, conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Retrieves all invoices for a specific client.

    Args:
        client_id: ID of the client whose invoices are to be retrieved.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        List of dictionaries with the client's invoice data.
    """
    try:
        query = """
            SELECT id, client_id, amount, issued_at, due_date, status
            FROM invoices
            WHERE client_id = $1
            ORDER BY id
        """
        rows = await conn.fetch(query, client_id)
        return [dict(row) for row in rows]
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in get_invoices_by_client_id: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_invoices_by_client_id: {e}")
        return []

@with_db_connection
async def create_invoice(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Creates a new invoice in the database.

    Args:
        invoice_data: InvoiceCreate model with the invoice data.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        Dictionary with the created invoice data.
    """
    try:
        query = """
            INSERT INTO invoices (client_id, amount, issued_at, due_date, status) 
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING id, client_id, amount, issued_at, due_date, status
        """
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
            logger.error("Could not create invoice")
            return {"success": False, "error": "Could not create invoice"}
        return dict(row)
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in create_invoice: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in create_invoice: {e}")
        return {"success": False, "error": str(e)}

@with_db_connection
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Updates the data of an existing invoice.

    Args:
        invoice_id: ID of the invoice to update.
        invoice_data: InvoiceUpdate model with the fields to update.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        Dictionary with the updated invoice data or None if not found.
        If the provided client_id does not exist, returns a clear error.
    """
    try:
        current_invoice = await get_invoice_by_id(invoice_id, conn=conn)
        if not current_invoice:
            logger.info(f"Invoice with ID {invoice_id} not found for update")
            return None
        update_fields = invoice_data.model_dump(exclude_unset=True)
        if not update_fields:
            logger.info(f"No fields to update for invoice ID {invoice_id}")
            return current_invoice
        # Validate that the client_id exists if provided
        if 'client_id' in update_fields:
            client_exists = await get_client_by_id(update_fields['client_id'], conn=conn)
            if not client_exists:
                logger.error(f"The client_id {update_fields['client_id']} does not exist. Cannot update invoice.")
                return {"success": False, "error": f"The client_id {update_fields['client_id']} does not exist."}
        set_clauses = []
        values = []
        for idx, (key, value) in enumerate(update_fields.items(), start=1):
            set_clauses.append(f"{key} = ${idx}")
            values.append(value)
        values.append(invoice_id)
        set_clause_str = ', '.join(set_clauses)
        id_placeholder = f"${len(values)}"
        query = f"""
            UPDATE invoices 
            SET {set_clause_str} 
            WHERE id = {id_placeholder}
            RETURNING id, client_id, amount, issued_at, due_date, status
        """
        row = await conn.fetchrow(query, *values)
        return dict(row) if row else None
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in update_invoice: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in update_invoice: {e}")
        return None

@with_db_connection
async def delete_invoice(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> bool:
    """
    Deletes an invoice from the database.

    Args:
        invoice_id: ID of the invoice to delete.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        Boolean indicating if the deletion was successful.
    """
    try:
        invoice = await get_invoice_by_id(invoice_id, conn=conn)
        if not invoice:
            logger.info(f"Invoice with ID {invoice_id} not found for deletion")
            return False
        query = "DELETE FROM invoices WHERE id = $1"
        result = await conn.execute(query, invoice_id)
        return "DELETE" in result
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in delete_invoice: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in delete_invoice: {e}")
        return False

@db_transaction
async def create_invoice_with_verification(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Creates a new invoice verifying beforehand that the client exists, within a transaction.

    Args:
        invoice_data: InvoiceCreate model with the invoice data.
        conn: Optional database connection. If not provided, a new one is created.
    Returns:
        Dictionary with the created invoice data or an error if the client does not exist.
    """
    try:
        client = await conn.fetchrow(
            "SELECT id FROM clients WHERE id = $1",
            invoice_data.client_id
        )
        if not client:
            error_msg = f"Cannot create invoice: client with ID {invoice_data.client_id} does not exist"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        # Reuse the insertion logic
        return await create_invoice(invoice_data, conn=conn)
    except asyncpg.PostgresError as e:
        logger.error(f"Database error in create_invoice_with_verification: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in create_invoice_with_verification: {e}")
        return {"success": False, "error": str(e)} 