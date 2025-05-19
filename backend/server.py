"""
Servidor principal de la aplicación MCP (Model Context Protocol).
Configura el ciclo de vida de la aplicación y registra las herramientas disponibles.
"""

import logging
from backend.core.database import database
from mcp.server.fastmcp import FastMCP
from backend.api.v1.tools.client_tools import register_tools
from fastapi import APIRouter, HTTPException

# Router para endpoints de health
health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/")
async def health_check():
    """
    Endpoint de healthcheck que verifica el estado del servidor y la base de datos.
    """
    try:
        async with database.connection() as conn:
            # Verifica que la conexión a la base de datos funcione
            await conn.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


# Configuración de logging
logging.basicConfig(level=logging.INFO)  # Configura el nivel de logging
logger = logging.getLogger(__name__)  # Crea un logger para este módulo


# Ciclo de vida MCP: gestiona una pool de PostgreSQL compartida
async def app_lifespan(server: FastMCP):
    """
    Context manager para el ciclo de vida de la aplicación.
    Gestiona la conexión a la base de datos PostgreSQL.
    """
    logger.info("⏳ Conectando a PostgreSQL…")
    try:
        # Crear pool de conexiones
        await database.connect()
        logger.info("✅ Conexión a PostgreSQL establecida")
        yield database._pool
    except Exception as e:
        logger.error(f"❌ Error al conectar con PostgreSQL: {e}")
        raise
    finally:
        await database.disconnect()


# Instancia principal de FastMCP
mcp = FastMCP(name="AI-Client-Agent-MCP", lifespan=app_lifespan, routes=[health_router])

# Registrar tools
register_tools(mcp)

if __name__ == "__main__":
    print("🚀 Servidor MCP arrancando…", flush=True)
    mcp.run()
