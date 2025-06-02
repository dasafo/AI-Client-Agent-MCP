import asyncpg
import asyncio
from backend.core.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def init_managers():
    user = DB_USER
    password = DB_PASSWORD
    database = DB_NAME
    host = DB_HOST
    port = int(DB_PORT) if DB_PORT else 5432

    # Leer el SQL desde el archivo externo
    import os
    sql_path = os.path.join(os.path.dirname(__file__), '../../database/managers.sql')
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    conn = await asyncpg.connect(user=user, password=password, database=database, host=host, port=port)
    try:
        await conn.execute(sql)
        print('Tabla managers creada y registros insertados (si no existían).')
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_managers())
