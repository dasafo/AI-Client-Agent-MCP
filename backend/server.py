import logging
import os
from dotenv import load_dotenv
from backend.mcp_instance import mcp  # ← Este debe ser único
from backend.api.v1.tools import client_tools  # ← ¡Importa tus tools!
import sys
import datetime

with open("/home/david/Documents/AI/AI-Client-Agent-MCP/startup_env.log", "w") as f:
    f.write(f"sys.executable: {sys.executable}\n")
    f.write(f"sys.path: {sys.path}\n")
    f.write(f"os.environ.get('VIRTUAL_ENV'): {os.environ.get('VIRTUAL_ENV')}\n")

log_path = os.path.join(os.path.dirname(__file__), "..", "mcp_agent_debug.log")
log_path = os.path.abspath(log_path)

def log_mcp_agent(msg):
    with open(log_path, "a") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")

# Ejemplo de uso
log_mcp_agent("==== Arrancando agente MCP ====")
log_mcp_agent(f"CWD: {os.getcwd()}")
log_mcp_agent(f"sys.path: {sys.path}")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
HOST = os.getenv("SERVER_HOST", "localhost")
PORT = int(os.getenv("SERVER_PORT", 8000))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("Arrancando FastMCP en %s:%s …", HOST, PORT)
    mcp.run(
        #transport="streamable-http",
        transport="sse",
        host=HOST,
        port=PORT,
        path="/sse",
        log_level="info",
    )

#  /home/david/Documents/AI/AI-Client-Agent-MCP/.venv/bin/python -m backend.server 
