import asyncpg

async def save_report(conn, client_id, client_name, period, manager_email, manager_name, report_type, report_text):
    """
    Guarda un informe en la base de datos.

    Args:
        conn: Conexión activa a la base de datos.
        client_id: ID del cliente asociado (puede ser None).
        client_name: Nombre del cliente (puede ser None).
        period: Periodo del informe (puede ser None).
        manager_email: Email del manager destinatario.
        manager_name: Nombre del manager destinatario.
        report_type: Tipo de informe.
        report_text: Texto HTML del informe generado.
    Returns:
        Diccionario con success True/False y error si aplica.
    """
    try:
        await conn.execute(
            """
            INSERT INTO reports (client_id, client_name, period, manager_email, manager_name, report_type, report_text)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            client_id, client_name, period, manager_email, manager_name, report_type, report_text
        )
        return {"success": True}
    except asyncpg.PostgresError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def get_client_by_name(name: str, conn=None):
    """
    Busca un cliente por nombre exacto (case-insensitive).
    Args:
        name: Nombre del cliente a buscar.
        conn: Conexión opcional a la base de datos.
    Returns:
        Diccionario con los datos del cliente o None si no se encuentra.
    """
    if conn is not None:
        row = await conn.fetchrow(
            "SELECT id, name, city, email, created_at FROM clients WHERE LOWER(name) = LOWER($1)",
            name
        )
        return dict(row) if row else None
    else:
        from backend.core.database import database
        async with database.connection() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, city, email, created_at FROM clients WHERE LOWER(name) = LOWER($1)",
                name
            )
            return dict(row) if row else None

def filter_invoices_by_period(invoices, period):
    """
    Filtra una lista de facturas por periodo (año, mes, etc.) en el campo issued_at.
    Args:
        invoices: Lista de diccionarios de facturas.
        period: Cadena a buscar en issued_at (por ejemplo, '2024').
    Returns:
        Lista filtrada de facturas.
    """
    return [i for i in invoices if period in str(i.get('issued_at', ''))] 