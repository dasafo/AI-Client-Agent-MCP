from backend.core.database import database
from backend.models.invoice import InvoiceCreate, InvoiceUpdate # Para type hinting si es necesario
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date

async def get_all_invoices() -> List[Dict[str, Any]]:
    pool = await database.connect()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices ORDER BY id"
        )
        return [dict(row) for row in rows]

async def get_invoice_by_id(invoice_id: int) -> Optional[Dict[str, Any]]:
    pool = await database.connect()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices WHERE id = $1",
            invoice_id
        )
        return dict(row) if row else None

async def get_invoices_by_client_id(client_id: int) -> List[Dict[str, Any]]:
    pool = await database.connect()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices WHERE client_id = $1 ORDER BY id",
            client_id
        )
        return [dict(row) for row in rows]

async def create_invoice(invoice_data: InvoiceCreate) -> Dict[str, Any]:
    pool = await database.connect()
    async with pool.acquire() as conn:
        # Valores por defecto de la base de datos para issued_at y status se aplicarán si no se proporcionan
        row = await conn.fetchrow(
            """
            INSERT INTO invoices (client_id, amount, issued_at, due_date, status) 
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING id, client_id, amount, issued_at, due_date, status
            """,
            invoice_data.client_id, 
            invoice_data.amount,
            invoice_data.issued_at if invoice_data.issued_at is not None else date.today(), # Default si no está en DDL
            invoice_data.due_date,
            invoice_data.status if invoice_data.status is not None else 'pending' # Default si no está en DDL
        )
        if not row:
            raise Exception("No se pudo crear la factura") # O un error más específico
        return dict(row)

async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate) -> Optional[Dict[str, Any]]:
    current_invoice = await get_invoice_by_id(invoice_id)
    if not current_invoice:
        return None

    # Crear un diccionario con los datos a actualizar, solo con los proporcionados
    update_fields = invoice_data.model_dump(exclude_unset=True)
    if not update_fields:
        return current_invoice # No hay nada que actualizar, devolver el actual

    # Construir la query dinámicamente
    set_clauses = []
    values = []
    i = 1
    for key, value in update_fields.items():
        set_clauses.append(f"{key} = ${i}")
        values.append(value)
        i += 1
    
    values.append(invoice_id) # Para el WHERE id = $i
    
    query = f"""
        UPDATE invoices 
        SET {', '.join(set_clauses)} 
        WHERE id = ${i}
        RETURNING id, client_id, amount, issued_at, due_date, status
    """
    
    pool = await database.connect()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(query, *values)
        return dict(row) if row else None

async def delete_invoice(invoice_id: int) -> bool:
    current_invoice = await get_invoice_by_id(invoice_id)
    if not current_invoice:
        return False # No existe, no se puede eliminar
    
    pool = await database.connect()
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM invoices WHERE id = $1", invoice_id)
        return result == "DELETE 1" 