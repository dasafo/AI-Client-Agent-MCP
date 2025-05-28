# Intentar importar FastMCP de fastmcp o mcp
try:
    from fastmcp import FastMCP
except ImportError:
    try:
        from mcp import FastMCP
    except ImportError:
        # Si falla, usar nuestro wrapper simple
        from backend.fastmcp_wrapper import SimpleFastMCP as FastMCP
        print("AVISO: Usando SimpleFastMCP como alternativa")

mcp = FastMCP(
    "AI-Client-Agent-MCP",
    stateless_http=True,
)
