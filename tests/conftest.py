# tests/conftest.py
import pytest
import asyncpg
import os
from backend.core.logging import get_logger
import pytest_asyncio

# Logger para los tests
logger = get_logger(__name__)

# Archivo de configuración para pytest
# Define fixtures y configuración para las pruebas, especialmente la gestión
# de la base de datos de prueba y las conexiones asíncronas

# Determina el directorio raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carga el archivo .env del directorio raíz del proyecto
# Esto permite usar DB_USER, DB_PASSWORD del .env principal como valores por defecto para las pruebas
# si no se establecen variables específicas DB_USER_TEST, etc. en otro lugar (por ejemplo, en variables de entorno de CI)
dotenv_path = os.path.join(PROJECT_ROOT, '.env')
if os.path.exists(dotenv_path):
    logger.info(f"Loading environment variables from: {dotenv_path}")
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_path)
else:
    logger.warning(f".env file not found at {dotenv_path}. Using system environment variables or defaults.")

# Opcional: Carga .env.test si existe, para sobrescribir configuraciones específicas para pruebas
dotenv_test_path = os.path.join(PROJECT_ROOT, 'tests', '.env.test') # O simplemente os.path.join(PROJECT_ROOT, '.env.test')
if os.path.exists(dotenv_test_path):
    logger.info(f"Loading test-specific environment variables from: {dotenv_test_path}")
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=dotenv_test_path, override=True) # override=True asegura que estas tengan precedencia

# Detalles de conexión a la base de datos de PRUEBA
# Es MUY recomendable usar una base de datos separada para pruebas
# para evitar pérdida accidental de datos en tu base de datos de desarrollo o producción.
from backend.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
TEST_DB_USER = os.getenv("DB_USER_TEST", DB_USER or "david")
TEST_DB_PASSWORD = os.getenv("DB_PASSWORD_TEST", DB_PASSWORD or "freedom85")
TEST_DB_HOST = os.getenv("DB_HOST_TEST", DB_HOST or "localhost")
TEST_DB_PORT = os.getenv("DB_PORT_TEST", DB_PORT or "5432")
TEST_DB_NAME = os.getenv("DB_NAME_TEST", "ai_client_mcp_db_test") # IMPORTANTE: Usar un nombre específico para la DB de prueba

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_CREATE_TABLES_PATH = os.path.join(BASE_DIR, "database", "create_tables.sql")

async def create_test_db_if_not_exists():
    """
    Crea la base de datos de prueba si no existe.
    
    Se conecta a la base de datos 'postgres' del sistema para crear la base de datos 
    de prueba si aún no existe.
    """
    conn_sys = None
    try:
        # Conecta a una base de datos del sistema (como 'postgres' o 'template1') para crear la base de datos de prueba
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

# Este fixture se mantiene con scope="session" para reutilización eficiente
@pytest_asyncio.fixture(scope="session")
async def db_engine_pool():
    """
    Fixture con alcance de sesión para crear una base de datos de prueba (si es necesario),
    establecer un pool de conexiones, crear tablas y realizar la limpieza al finalizar.
    
    Este fixture gestiona el ciclo de vida completo de la base de datos de prueba:
    1. Creación de la BD si no existe
    2. Aplicación del esquema de tablas
    3. Provisión del pool de conexiones para los tests
    4. Eliminación de la BD al finalizar todos los tests
    """
    await create_test_db_if_not_exists() # Asegura que la BD de prueba existe

    # Crea un pool de conexiones a la BD de prueba
    pool = await asyncpg.create_pool(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT,
        min_size=1, max_size=5
    )
    
    try:
        # Aplica el esquema SQL a la BD de prueba
        async with pool.acquire() as connection:
            logger.info(f"Applying schema from {SQL_CREATE_TABLES_PATH} to test database {TEST_DB_NAME}...")
            with open(SQL_CREATE_TABLES_PATH, "r") as f:
                await connection.execute(f.read())
            logger.info("Schema applied.")
        
        yield pool # Proporciona el pool a los fixtures/tests dependientes
        
    finally:
        # Limpieza al finalizar todos los tests
        logger.info(f"Closing connection pool for test database {TEST_DB_NAME}...")
        await pool.close()
        
        # Elimina la base de datos de prueba después de que todos los tests de la sesión hayan terminado
        conn_sys = None
        try:
            # Conecta a una base de datos del sistema para eliminar la base de datos de prueba
            conn_sys = await asyncpg.connect(
                user=TEST_DB_USER, password=TEST_DB_PASSWORD,
                host=TEST_DB_HOST, port=TEST_DB_PORT, database='postgres' # Conecta a la BD 'postgres' predeterminada
            )
            logger.info(f"Dropping test database {TEST_DB_NAME}...")
            # Es importante asegurar que no haya otras conexiones activas.
            # La desconexión forzada de otros usuarios puede hacerse con:
            # await conn_sys.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{TEST_DB_NAME}';")
            # Sin embargo, esto es agresivo. DROP DATABASE debería funcionar si el pool se cierra correctamente.
            await conn_sys.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"')
            logger.info(f"Test database '{TEST_DB_NAME}' dropped.")
        except Exception as e:
            logger.error(f"ERROR: Could not drop test database '{TEST_DB_NAME}'. It might be in use or not exist. {e}")
            logger.error("You might need to drop it manually if issues persist.")
        finally:
            if conn_sys:
                await conn_sys.close()

# Restauramos la dependencia en db_engine_pool para asegurar secuencia correcta,
# pero mantenemos la conexión directa
@pytest_asyncio.fixture
async def db_conn(db_engine_pool):  # Añadimos db_engine_pool como parámetro
    """
    Fixture con alcance de función que crea una conexión directa a la base de datos de prueba,
    inicia una transacción y la revierte después de la prueba.
    
    Toma db_engine_pool como parámetro para asegurar que la base de datos de prueba esté creada
    antes de intentar conectarse, pero crea su propia conexión directa para evitar
    problemas de alcance.
    
    Este fixture proporciona aislamiento de prueba mediante transacciones:
    1. Cada test recibe su propia conexión con una transacción activa
    2. Los cambios hechos durante el test no afectan a otros tests
    3. La transacción se revierte al finalizar, dejando la BD limpia
    """
    # Conexión directa a la DB de prueba, sin usar el pool
    conn = await asyncpg.connect(
        user=TEST_DB_USER, password=TEST_DB_PASSWORD,
        database=TEST_DB_NAME, host=TEST_DB_HOST, port=TEST_DB_PORT
    )

    # Inicia una transacción para aislar los cambios de este test
    transaction = conn.transaction()
    await transaction.start()
    logger.info("DB transaction started for test.")
    
    try:
        yield conn # Proporciona la conexión a la función de test
    finally:
        # Revierte la transacción después de que el test haya terminado
        logger.info("Rolling back DB transaction for test.")
        await transaction.rollback()
        logger.info("DB transaction rolled back.")
        
        # Cierra la conexión
        await conn.close()
        logger.info("DB connection closed.")
