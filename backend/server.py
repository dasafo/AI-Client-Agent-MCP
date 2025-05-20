"""
Servidor principal de la aplicación MCP (Model Context Protocol).
Configura el ciclo de vida de la aplicación y registra las herramientas disponibles.
"""

from fastmcp import FastMCP
from backend.api.v1.tools.client_tools import register_tools

mcp = FastMCP(name="AI-Client-Agent-MCP")
register_tools(mcp)

if __name__ == "__main__":
    print("🚀 Servidor MCP arrancando…", flush=True)
    mcp.run(host="0.0.0.0", port=8000, transport="streamable-http")
