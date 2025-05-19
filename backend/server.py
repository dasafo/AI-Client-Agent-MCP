"""
Servidor principal de la aplicación MCP (Model Context Protocol).
Configura el ciclo de vida de la aplicación y registra las herramientas disponibles.
"""
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import asyncpg
from mcp.server.fastmcp import FastMCP

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importaciones locales
from backend.core.config import settings
from backend.api.tools.client_tools import register_tools

# Ciclo de vida MCP: gestiona una pool de PostgreSQL compartida
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[asyncpg.Pool]:
    """
    Context manager para el ciclo de vida de la aplicación.
    Gestiona la conexión a la base de datos PostgreSQL.
    """
    logger.info("⏳ Conectando a PostgreSQL…")
    try:
        pool = await asyncpg.create_pool(
            dsn=settings.DATABASE_URL,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        if not pool:
            raise RuntimeError("No se pudo conectar a la base de datos")
            
        logger.info("✅ Conexión a PostgreSQL establecida")
        yield pool
        
    except Exception as e:
        logger.error(f"❌ Error al conectar con PostgreSQL: {e}")
        raise
        
    finally:
        if 'pool' in locals() and pool:
            logger.info("🛑 Cerrando pool de conexiones PostgreSQL…")
            await pool.close()

# Instancia principal de FastMCP
mcp = FastMCP(
    name="AI-Client-Agent-MCP",
    lifespan=app_lifespan,
    dependencies=["asyncpg"],
)

# Registrar tools
register_tools(mcp)

if __name__ == "__main__":
    print("🚀 Servidor MCP arrancando…", flush=True)
    mcp.run()
