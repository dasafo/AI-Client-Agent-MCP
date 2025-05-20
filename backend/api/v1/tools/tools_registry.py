# tools_registry.py
"""
Registro automático de tools MCP mediante decorador.
"""

TOOLS = []


def mcp_tool(name: str, description: str):
    def decorator(func):
        TOOLS.append((func, name, description))
        return func

    return decorator
