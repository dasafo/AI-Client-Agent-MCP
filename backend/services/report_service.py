import asyncpg

async def save_report(conn, client_id, client_name, period, manager_email, manager_name, report_type, report_text):
    await conn.execute(
        """
        INSERT INTO reports (client_id, client_name, period, manager_email, manager_name, report_type, report_text)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        """,
        client_id, client_name, period, manager_email, manager_name, report_type, report_text
    ) 