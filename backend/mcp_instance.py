# backend/mcp_instance.py
# Definición de la instancia central del Master Control Program (MCP)

# Intentar importar FastMCP de fastmcp o mcp
try:
    from fastmcp import FastMCP
except ImportError:
    try:
        from mcp import FastMCP
    except ImportError:
        print("ERROR CRÍTICO: No se pudo importar FastMCP ni de 'fastmcp' ni de 'mcp'.")
        print("Asegúrate de que uno de estos paquetes esté instalado correctamente en tu entorno.")
        raise

# Crear una instancia única de FastMCP para toda la aplicación
# Esta instancia centralizada permite registrar todas las herramientas (tools)
# y manejar las solicitudes de los clientes
mcp = FastMCP(
    "AI-Client-Agent-MCP",  # Nombre del agente MCP
    stateless_http=True,    # Configuración para manejo HTTP sin estado
)

# # Opcionalmente, exponer la aplicación FastAPI directamente para Uvicorn
# app = mcp.app
