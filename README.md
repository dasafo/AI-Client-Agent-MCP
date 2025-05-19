# AI-Client-Agent-MCP

Un agente MCP profesional para gestión y consulta de clientes usando Python, PostgreSQL y el protocolo Model Context Protocol (MCP).

## 🚀 Características principales

- Consultar clientes por email, añadir nuevos, etc.
- Preparado para ampliación: más tablas, análisis, emails, integraciones externas.
- Modular y profesional: separación clara entre server, tools, database y docs.
- Compatible con Cursor, Windsurf, Claude y otros agentes MCP modernos (usando `"command"`/`"args"` en la config MCP).

## 📦 Estructura

- **backend/**: código principal de servidor y tools
- **database/**: scripts de modelo de datos y ejemplo
- **docs/**: documentación técnica y de uso
- **tests/**: tests unitarios
- **README.md**: este archivo

## 🛠️ Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
