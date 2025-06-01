import asyncpg
import asyncio

SQL = '''
CREATE TABLE IF NOT EXISTS managers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT, -- opcional: gerente, dueño, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO managers (name, email, role)
SELECT * FROM (VALUES
    ('David Salas', 'd.salasforns@gmail.com', 'boss'),
    ('Pedro Salas', 'dsf@protonmail.com', 'boss'),
    ('Ana Ruiz', 'ana.ruiz@empresa.com', 'manager'),
    ('Luis Martínez', 'luis.martinez@negocio.com', 'manager')
) AS v(name, email, role)
WHERE NOT EXISTS (
    SELECT 1 FROM managers WHERE managers.email = v.email
);
'''

async def init_managers():
    import os
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    host = os.getenv('DB_HOST')
    port = int(os.getenv('DB_PORT', 5432))
    conn = await asyncpg.connect(user=user, password=password, database=database, host=host, port=port)

    try:
        await conn.execute(SQL)
        print('Tabla managers creada y registros insertados (si no existían).')
    finally:
        await conn.close()

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(init_managers())
