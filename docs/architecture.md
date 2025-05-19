# Arquitectura del Proyecto

- Servidor MCP Python usando FastMCP
- Conexión pool a PostgreSQL, compartida por todas las tools
- Tools registradas en módulos separados para facilitar escalado
- Compatible con MCP agents (Claude, Cursor, Windsurf, etc.)