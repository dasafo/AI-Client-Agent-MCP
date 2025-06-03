# tests/conftest.py
import pytest
import asyncpg
import os
from backend.core.logging import get_logger
import pytest_asyncio

# Logger for tests
logger = get_logger(__name__)

# Configuration file for pytest
# Defines fixtures and configuration for tests, especially the management
# of the test database and asynchronous connections

# Determines the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Loads the .env file from the project root directory
# This allows using DB_USER, DB_PASSWORD from the main .env as default values for tests
# if specific variables DB_USER_TEST, etc. are not set elsewhere (e.g., in CI environment variables)
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
if os.path.exists(dotenv_path):
    logger.info(f"Loading environment variables from: {dotenv_path}")
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_path)
else:
    logger.warning(f".env file not found at {dotenv_path}. Using system environment variables or defaults.")

# Optional: Load .env.test if it exists, to override specific test configurations
dotenv_test_path = os.path.join(PROJECT_ROOT, 'tests', '.env.test') # Or simply os.path.join(PROJECT_ROOT, '.env.test')
if os.path.exists(dotenv_test_path):
    logger.info(f"Loading test-specific environment variables from: {dotenv_test_path}")
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_test_path, override=True) # override=True ensures these take precedence

# Test database connection details
# It is HIGHLY recommended to use a separate database for tests
# to avoid accidental data loss in your development or production database.
from backend.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
TEST_DB_USER = os.getenv("DB_USER_TEST", DB_USER or "david")
TEST_DB_PASSWORD = os.getenv("DB_PASSWORD_TEST", DB_PASSWORD or "freedom85")
TEST_DB_HOST = os.getenv("DB_HOST_TEST", DB_HOST or "localhost")
TEST_DB_PORT = os.getenv("DB_PORT_TEST", DB_PORT or "5432")
TEST_DB_NAME = os.getenv("DB_NAME_TEST", "ai_client_mcp_db_test") # IMPORTANT: Use a specific name for the test DB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_CREATE_TABLES_PATH = os.path.join(BASE_DIR, "database", "create_tables.sql")

async def create_test_db_if_not_exists():
    """
    Creates the test database if it does not exist.
    
    Connects to the system 'postgres' database to create the test database
    if it does not already exist.
    """
    conn_sys = None
    try:
        # Connects to a system database (like 'postgres' or 'template1') to create the test database
        conn_sys = await asyncpg.connect(
            user=TEST_DB_USER, password=TEST_DB_PASSWORD,
            host=TEST_DB_HOST, port=TEST_DB_PORT, database='postgres'
        )
        exists = await conn_sys.fetchval(f"SELECT 1 FROM pg_database WHERE datname = $1", TEST_DB_NAME)
        if not exists:
            logger.info(f"Creating test database: {TEST_DB_NAME}...")
            await conn_sys.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
            logger.info(f"Test database '{TEST_DB_NAME}' created.")
        else:
            logger.info(f"Test database '{TEST_DB_NAME}' already exists.")
    except Exception as e:
        logger.error(f"ERROR: Could not connect to system DB or create test DB '{TEST_DB_NAME}'. {e}")
        logger.error("Please ensure your PostgreSQL server is running, accessible, and the user has permissions,")
        logger.error(f"or create the test database '{TEST_DB_NAME}' manually.")
        raise
    finally:
        if conn_sys:
            await conn_sys.close()

# This fixture is kept with scope="session" for efficient reuse
@pytest_asyncio.fixture(scope="session")
async def db_engine_pool():
    """
    Session-scoped fixture to create a test database (if necessary),
    establish a connection pool, create tables, and perform cleanup at the end.
    
    This fixture manages the full lifecycle of the test database:
    1. Creation of the DB if it does not exist
    2. Application of the table schema
    3. Provision of the connection pool for tests
    4. Deletion of the DB after all tests are finished
    """
    await create_test_db_if_not_exists() # Ensures the test DB exists

    # Creates a connection pool to the test DB
    pool = await asyncpg.create_pool(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT,
        min_size=1, max_size=5
    )
    
    try:
        # Applies the SQL schema to the test DB
        async with pool.acquire() as connection:
            logger.info(f"Applying schema from {SQL_CREATE_TABLES_PATH} to test database {TEST_DB_NAME}...")
            with open(SQL_CREATE_TABLES_PATH, "r") as f:
                await connection.execute(f.read())
            logger.info("Schema applied.")
        
        yield pool # Provide the pool to dependent fixtures/tests
        
    finally:
        # Cleanup at the end of all tests
        logger.info(f"Closing connection pool for test database {TEST_DB_NAME}...")
        await pool.close()
        
        # Deletes the test database after all session tests are finished
        conn_sys = None
        try:
            # Connects to a system database to delete the test database
            conn_sys = await asyncpg.connect(
                user=TEST_DB_USER, password=TEST_DB_PASSWORD,
                host=TEST_DB_HOST, port=TEST_DB_PORT, database='postgres' # Connects to the default 'postgres' DB
            )
            logger.info(f"Dropping test database {TEST_DB_NAME}...")
            # It is important to ensure there are no other active connections.
            # Forced disconnection of other users can be done with:
            # await conn_sys.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{TEST_DB_NAME}';")
            # However, this is aggressive. DROP DATABASE should work if the pool is closed properly.
            await conn_sys.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"')
            logger.info(f"Test database '{TEST_DB_NAME}' dropped.")
        except Exception as e:
            logger.error(f"ERROR: Could not drop test database '{TEST_DB_NAME}'. It might be in use or not exist. {e}")
            logger.error("You might need to drop it manually if issues persist.")
        finally:
            if conn_sys:
                await conn_sys.close()

# Restore the dependency on db_engine_pool to ensure correct sequence,
# but keep the direct connection
@pytest_asyncio.fixture
async def db_conn(db_engine_pool):  # Added db_engine_pool as a parameter
    """
    Function-scoped fixture that creates a direct connection to the test database,
    starts a transaction, and rolls it back after the test.
    
    Takes db_engine_pool as a parameter to ensure the test database is created
    before attempting to connect, but creates its own direct connection to avoid
    scope issues.
    
    This fixture provides test isolation via transactions:
    1. Each test receives its own connection with an active transaction
    2. Changes made during the test do not affect other tests
    3. The transaction is rolled back at the end, leaving the DB clean
    """
    # Direct connection to the test DB, without using the pool
    conn = await asyncpg.connect(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT
    )

    # Start a transaction to isolate this test's changes
    transaction = conn.transaction()
    await transaction.start()
    logger.info("DB transaction started for test.")
    
    try:
        yield conn # Provide the connection to the test function
    finally:
        # Roll back the transaction after the test is finished
        logger.info("Rolling back DB transaction for test.")
        await transaction.rollback()
        logger.info("DB transaction rolled back.")
        
        # Close the connection
        await conn.close()
        logger.info("DB connection closed.")
