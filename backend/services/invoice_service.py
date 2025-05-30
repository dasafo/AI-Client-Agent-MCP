from backend.core.database import database
from backend.models.invoice import InvoiceCreate, InvoiceUpdate # Para type hinting si es necesario
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import date
import asyncpg

# Servicios para la gestión de facturas
# Estas funciones implementan la lógica de negocio y el acceso a la base de datos para las facturas
# Todas las funciones aceptan una conexión opcional para facilitar las transacciones y las pruebas

async def get_all_invoices(conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Obtiene todas las facturas ordenadas por ID.
    
    Args:
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Lista de diccionarios con los datos de todas las facturas.
    """
    # Conexión interna a gestionar si no se proporciona conn
    conn_for_read = None
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_read = await pool.acquire()
            conn_to_use = conn_for_read
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Consulta todas las facturas ordenadas por ID
        rows = await conn_to_use.fetch(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices ORDER BY id"
        )
        return [dict(row) for row in rows]
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_read:
            await pool.release(conn_for_read)

async def get_invoice_by_id(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Obtiene una factura específica por su ID.
    
    Args:
        invoice_id: ID de la factura a buscar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos de la factura o None si no se encuentra.
    """
    conn_for_read = None
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_read = await pool.acquire()
            conn_to_use = conn_for_read
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Consulta la factura por ID
        row = await conn_to_use.fetchrow(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices WHERE id = $1",
            invoice_id
        )
        return dict(row) if row else None
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_read:
            await pool.release(conn_for_read)

async def get_invoices_by_client_id(client_id: int, conn: Optional[asyncpg.Connection] = None) -> List[Dict[str, Any]]:
    """
    Obtiene todas las facturas de un cliente específico.
    
    Args:
        client_id: ID del cliente cuyos facturas se desean obtener.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Lista de diccionarios con los datos de las facturas del cliente.
    """
    conn_for_read = None
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_read = await pool.acquire()
            conn_to_use = conn_for_read
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Consulta las facturas del cliente ordenadas por ID
        rows = await conn_to_use.fetch(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices WHERE client_id = $1 ORDER BY id",
            client_id
        )
        return [dict(row) for row in rows]
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_read:
            await pool.release(conn_for_read)

async def create_invoice(invoice_data: InvoiceCreate, conn: Optional[asyncpg.Connection] = None) -> Dict[str, Any]:
    """
    Crea una nueva factura en la base de datos.
    
    Args:
        invoice_data: Objeto InvoiceCreate con los datos de la factura a crear.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos de la factura creada.
        
    Raises:
        Exception: Si no se pudo crear la factura.
    """
    conn_for_write = None
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_write = await pool.acquire()
            conn_to_use = conn_for_write
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Valores por defecto de la base de datos para issued_at y status se aplicarán si no se proporcionan
        row = await conn_to_use.fetchrow(
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
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_write:
            await pool.release(conn_for_write)

async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, conn: Optional[asyncpg.Connection] = None) -> Optional[Dict[str, Any]]:
    """
    Actualiza los datos de una factura existente.
    
    Args:
        invoice_id: ID de la factura a actualizar.
        invoice_data: Objeto InvoiceUpdate con los campos a actualizar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Diccionario con los datos actualizados de la factura o None si no se encuentra.
    """
    conn_for_write = None
    
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_write = await pool.acquire()
            conn_to_use = conn_for_write
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Verificar que existe la factura
        row = await conn_to_use.fetchrow(
            "SELECT id, client_id, amount, issued_at, due_date, status FROM invoices WHERE id = $1",
            invoice_id
        )
        current_invoice = dict(row) if row else None
        
        if not current_invoice:
            return None  # La factura no existe, no se puede actualizar

        # Crear un diccionario con los datos a actualizar, solo con los proporcionados
        update_fields = invoice_data.model_dump(exclude_unset=True)
        if not update_fields:
            return current_invoice # No hay nada que actualizar, devolver el actual

        # Construir la query dinámicamente para actualizar solo los campos proporcionados
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
        
        # Ejecuta la actualización y devuelve los datos actualizados
        row = await conn_to_use.fetchrow(query, *values)
        return dict(row) if row else None
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_write:
            await pool.release(conn_for_write)

async def delete_invoice(invoice_id: int, conn: Optional[asyncpg.Connection] = None) -> bool:
    """
    Elimina una factura de la base de datos.
    
    Args:
        invoice_id: ID de la factura a eliminar.
        conn: Conexión opcional a la base de datos. Si no se proporciona, se crea una nueva.
        
    Returns:
        Boolean indicando si la eliminación fue exitosa.
    """
    conn_for_delete = None
    
    try:
        if conn is None:
            # Si no hay una conexión proporcionada, obtenemos una nueva
            pool = await database.connect()
            conn_for_delete = await pool.acquire()
            conn_to_use = conn_for_delete
        else:
            # Usamos la conexión proporcionada
            conn_to_use = conn
            
        # Verificar que existe la factura
        row = await conn_to_use.fetchrow(
            "SELECT id FROM invoices WHERE id = $1",
            invoice_id
        )
        
        if not row:
            return False # La factura no existe, no se puede eliminar
        
        # Elimina la factura y verifica que se eliminó exactamente un registro
        result = await conn_to_use.execute("DELETE FROM invoices WHERE id = $1", invoice_id)
        return result == "DELETE 1" # Retorna True si se eliminó exactamente un registro
    finally:
        # Solo cerramos las conexiones que creamos internamente
        if conn_for_delete:
            await pool.release(conn_for_delete) 