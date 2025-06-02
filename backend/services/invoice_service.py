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
    Obtiene todas las facturas ordenadas por ID.

    Args:
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Lista de diccionarios con los datos de las facturas.
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
        logger.error(f"Error de base de datos en get_all_invoices: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado en get_all_invoices: {e}")
        return []

@with_db_connection
async def get_invoice_by_id(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Obtiene una factura específica por su ID.

    Args:
        invoice_id: ID de la factura a buscar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos de la factura o None si no se encuentra.
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
        logger.error(f"Error de base de datos en get_invoice_by_id: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado en get_invoice_by_id: {e}")
        return None

@with_db_connection
async def get_invoices_by_client_id(client_id: int, conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Obtiene todas las facturas de un cliente específico.

    Args:
        client_id: ID del cliente cuyas facturas se desean obtener.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Lista de diccionarios con los datos de las facturas del cliente.
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
        logger.error(f"Error de base de datos en get_invoices_by_client_id: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado en get_invoices_by_client_id: {e}")
        return []

@with_db_connection
async def create_invoice(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Crea una nueva factura en la base de datos.

    Args:
        invoice_data: Modelo InvoiceCreate con los datos de la factura.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos de la factura creada.
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
            logger.error("No se pudo crear la factura")
            return {"success": False, "error": "No se pudo crear la factura"}
        return dict(row)
    except asyncpg.PostgresError as e:
        logger.error(f"Error de base de datos en create_invoice: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error inesperado en create_invoice: {e}")
        return {"success": False, "error": str(e)}

@with_db_connection
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Actualiza los datos de una factura existente.

    Args:
        invoice_id: ID de la factura a actualizar.
        invoice_data: Modelo InvoiceUpdate con los campos a actualizar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos de la factura actualizada o None si no se encuentra.
        Si el client_id proporcionado no existe, devuelve un error claro.
    """
    try:
        current_invoice = await get_invoice_by_id(invoice_id, conn=conn)
        if not current_invoice:
            logger.info(f"Factura con ID {invoice_id} no encontrada para actualizar")
            return None
        update_fields = invoice_data.model_dump(exclude_unset=True)
        if not update_fields:
            logger.info(f"No hay campos para actualizar en la factura ID {invoice_id}")
            return current_invoice
        # Validar que el client_id exista si se proporciona
        if 'client_id' in update_fields:
            client_exists = await get_client_by_id(update_fields['client_id'], conn=conn)
            if not client_exists:
                logger.error(f"El client_id {update_fields['client_id']} no existe. No se puede actualizar la factura.")
                return {"success": False, "error": f"El client_id {update_fields['client_id']} no existe."}
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
        logger.error(f"Error de base de datos en update_invoice: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado en update_invoice: {e}")
        return None

@with_db_connection
async def delete_invoice(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> bool:
    """
    Elimina una factura de la base de datos.

    Args:
        invoice_id: ID de la factura a eliminar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Booleano que indica si la eliminación fue exitosa.
    """
    try:
        invoice = await get_invoice_by_id(invoice_id, conn=conn)
        if not invoice:
            logger.info(f"Factura con ID {invoice_id} no encontrada para eliminar")
            return False
        query = "DELETE FROM invoices WHERE id = $1"
        result = await conn.execute(query, invoice_id)
        return "DELETE" in result
    except asyncpg.PostgresError as e:
        logger.error(f"Error de base de datos en delete_invoice: {e}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado en delete_invoice: {e}")
        return False

@db_transaction
async def create_invoice_with_verification(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Crea una nueva factura verificando previamente que el cliente exista, dentro de una transacción.

    Args:
        invoice_data: Modelo InvoiceCreate con los datos de la factura.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
    Returns:
        Diccionario con los datos de la factura creada o un error si el cliente no existe.
    """
    try:
        client = await conn.fetchrow(
            "SELECT id FROM clients WHERE id = $1",
            invoice_data.client_id
        )
        if not client:
            error_msg = f"No se puede crear la factura: el cliente con ID {invoice_data.client_id} no existe"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        # Reutiliza la lógica de inserción
        return await create_invoice(invoice_data, conn=conn)
    except asyncpg.PostgresError as e:
        logger.error(f"Error de base de datos en create_invoice_with_verification: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"Error inesperado en create_invoice_with_verification: {e}")
        return {"success": False, "error": str(e)} 