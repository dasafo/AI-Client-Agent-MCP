import asyncpg

async def save_report(conn, client_id, client_name, period, manager_email, manager_name, report_type, report_text):
    """
    Saves a report in the database.

    Args:
        conn: Active database connection.
        client_id: Associated client ID (can be None).
        client_name: Client name (can be None).
        period: Report period (can be None).
        manager_email: Recipient manager's email.
        manager_name: Recipient manager's name.
        report_type: Report type.
        report_text: Generated HTML report text.
    Returns:
        Dictionary with success True/False and error if applicable.
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
    Searches for a client by exact name (case-insensitive).
    Args:
        name: Name of the client to search for.
        conn: Optional database connection.
    Returns:
        Dictionary with client data or None if not found.
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
    Filters a list of invoices by period (year, month, etc.) in the issued_at field.
    Args:
        invoices: List of invoice dictionaries.
        period: String to search for in issued_at (e.g., '2024').
    Returns:
        Filtered list of invoices.
    """
    return [i for i in invoices if period in str(i.get('issued_at', ''))] 