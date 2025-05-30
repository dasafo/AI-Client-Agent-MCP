# tests/conftest.py
import pytest
import asyncpg
import os
from dotenv import load_dotenv
import pytest_asyncio

# Determine the root directory of the project (e.g., where .env might be)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load .env file from the project root
# This allows DB_USER, DB_PASSWORD from your main .env to be used as defaults for tests
# if specific DB_USER_TEST etc. are not set elsewhere (e.g. CI environment variables)
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
if os.path.exists(dotenv_path):
    print(f"Loading environment variables from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f".env file not found at {dotenv_path}. Using system environment variables or defaults.")

# Optional: Load .env.test if it exists, to override settings specifically for tests
dotenv_test_path = os.path.join(PROJECT_ROOT, 'tests', '.env.test') # Or just os.path.join(PROJECT_ROOT, '.env.test')
if os.path.exists(dotenv_test_path):
    print(f"Loading test-specific environment variables from: {dotenv_test_path}")
    load_dotenv(dotenv_path=dotenv_test_path, override=True) # override=True ensures these take precedence

# Database connection details for the TEST DATABASE
# It's STRONGLY recommended to use a separate database for testing
# to avoid accidental data loss in your development or production DB.
TEST_DB_USER = os.getenv("DB_USER_TEST", os.getenv("DB_USER", "david"))
TEST_DB_PASSWORD = os.getenv("DB_PASSWORD_TEST", os.getenv("DB_PASSWORD", "freedom85"))
TEST_DB_HOST = os.getenv("DB_HOST_TEST", os.getenv("DB_HOST", "localhost"))
TEST_DB_PORT = os.getenv("DB_PORT_TEST", os.getenv("DB_PORT", "5432"))
TEST_DB_NAME = os.getenv("DB_NAME_TEST", "ai_client_mcp_db_test") # IMPORTANT: Use a test-specific DB name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_CREATE_TABLES_PATH = os.path.join(BASE_DIR, "database", "create_tables.sql")

async def create_test_db_if_not_exists():
    """Creates the test database if it doesn't exist."""
    conn_sys = None
    try:
        # Connect to a system database (like 'postgres' or 'template1') to create the test database
        conn_sys = await asyncpg.connect(
            user=TEST_DB_USER, password=TEST_DB_PASSWORD,
            host=TEST_DB_HOST, port=TEST_DB_PORT, database='postgres'
        )
        exists = await conn_sys.fetchval(f"SELECT 1 FROM pg_database WHERE datname = $1", TEST_DB_NAME)
        if not exists:
            print(f"Creating test database: {TEST_DB_NAME}...")
            await conn_sys.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
            print(f"Test database '{TEST_DB_NAME}' created.")
        else:
            print(f"Test database '{TEST_DB_NAME}' already exists.")
    except Exception as e:
        print(f"ERROR: Could not connect to system DB or create test DB '{TEST_DB_NAME}'. {e}")
        print("Please ensure your PostgreSQL server is running, accessible, and the user has permissions,")
        print(f"or create the test database '{TEST_DB_NAME}' manually.")
        raise
    finally:
        if conn_sys:
            await conn_sys.close()

# Este fixture se mantiene con scope="session" para reutilización eficiente
@pytest_asyncio.fixture(scope="session")
async def db_engine_pool():
    """
    Session-scoped fixture to create a test database (if needed),
    establish a connection pool, create tables, and tear down.
    """
    await create_test_db_if_not_exists() # Ensure the test DB exists

    pool = await asyncpg.create_pool(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT,
        min_size=1, max_size=5
    )
    
    try:
        async with pool.acquire() as connection:
            print(f"Applying schema from {SQL_CREATE_TABLES_PATH} to test database {TEST_DB_NAME}...")
            with open(SQL_CREATE_TABLES_PATH, "r") as f:
                await connection.execute(f.read())
            print("Schema applied.")
        
        yield pool # Provide the pool to dependent fixtures/tests
        
    finally:
        print(f"Closing connection pool for test database {TEST_DB_NAME}...")
        await pool.close()
        # Drop the test database after all tests in the session are done
        conn_sys = None
        try:
            # Connect to a system database (like 'postgres' or 'template1') to drop the test database
            conn_sys = await asyncpg.connect(
                user=TEST_DB_USER, password=TEST_DB_PASSWORD,
                host=TEST_DB_HOST, port=TEST_DB_PORT, database='postgres' # Connect to default 'postgres' db
            )
            print(f"Dropping test database {TEST_DB_NAME}...")
            # It's important to ensure no other connections are active.
            # Forcing disconnection of other users can be done with:
            # await conn_sys.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{TEST_DB_NAME}';")
            # However, this is aggressive. DROP DATABASE should work if the pool is properly closed.
            await conn_sys.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"')
            print(f"Test database '{TEST_DB_NAME}' dropped.")
        except Exception as e:
            print(f"ERROR: Could not drop test database '{TEST_DB_NAME}'. It might be in use or not exist. {e}")
            print("You might need to drop it manually if issues persist.")
        finally:
            if conn_sys:
                await conn_sys.close()

# Restauramos la dependencia en db_engine_pool para asegurar secuencia correcta,
# pero mantenemos la conexión directa
@pytest_asyncio.fixture
async def db_conn(db_engine_pool):  # Añadimos db_engine_pool como parámetro
    """
    Function-scoped fixture that creates a direct connection to the test database,
    starts a transaction, and rolls it back after the test.
    
    Takes db_engine_pool as a parameter to ensure the test database is created
    before trying to connect, but creates its own direct connection to avoid
    scope issues.
    """
    # Conexión directa a la DB de prueba, sin usar el pool
    conn = await asyncpg.connect(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT
    )

    transaction = conn.transaction()
    await transaction.start()
    print("DB transaction started for test.")
    
    try:
        yield conn # Provide the connection to the test function
    finally:
        # Rollback the transaction after the test is done
        print("Rolling back DB transaction for test.")
        await transaction.rollback()
        print("DB transaction rolled back.")
        
        # Close the connection
        await conn.close()
        print("DB connection closed.")
