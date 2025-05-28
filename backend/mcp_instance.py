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

mcp = FastMCP(
    "AI-Client-Agent-MCP",
    stateless_http=True,
)
