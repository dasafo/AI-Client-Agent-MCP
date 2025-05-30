import logging
import os
from dotenv import load_dotenv
from backend.mcp_instance import mcp  # ← Este debe ser único
from backend.api.v1.tools import client_tools  # Importa tus tools de clientes
from backend.api.v1.tools import invoice_tools # Importa tus tools de facturas
import sys
import datetime

# Archivo principal del servidor para AI Client Agent MCP
# Configura y arranca el servidor FastMCP con todas las herramientas registradas

# Log de inicio - Modificado para Docker
# Directorio de logs dentro de /app (directorio de trabajo en Docker)
LOGS_DIR = "/app/logs" # O simplemente "logs" si quieres que sea relativo a /app
STARTUP_DETAILS_LOG_PATH = os.path.join(LOGS_DIR, "startup_server_details.log")

# Asegurarse de que el directorio de logs exista
if not os.path.exists(LOGS_DIR):
    try:
        os.makedirs(LOGS_DIR)
    except OSError as e:
        # En un entorno serverless o muy restringido, esto podría fallar.
        # Para Docker, generalmente está bien.
        print(f"Warning: Could not create logs directory {LOGS_DIR}: {e}", file=sys.stderr)
        # Fallback a log en /app si la creación del subdir falla
        STARTUP_DETAILS_LOG_PATH = "/app/startup_server_details.log"

# Guardar detalles de inicio para ayudar en la depuración
try:
    with open(STARTUP_DETAILS_LOG_PATH, "w") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] Server starting up...\n")
        f.write(f"sys.executable: {sys.executable}\n")
        f.write(f"sys.path: {str(sys.path)}\n") # Convertir sys.path a string
        f.write(f"os.getcwd(): {os.getcwd()}\n")
        f.write(f"os.environ.get('VIRTUAL_ENV'): {os.environ.get('VIRTUAL_ENV')}\n")
except IOError as e:
    print(f"Warning: Could not write to {STARTUP_DETAILS_LOG_PATH}: {e}", file=sys.stderr)


# Ruta para mcp_agent_debug.log - se resolverá a /app/logs/mcp_agent_debug.log
DEBUG_LOG_PATH = os.path.join(LOGS_DIR, "mcp_agent_debug.log")

# Función para registrar mensajes en el log de depuración
def log_mcp_agent(msg):
    """
    Registra mensajes en el archivo de log de depuración del agente MCP.
    
    Args:
        msg: Mensaje a registrar en el log.
    """
    try:
        with open(DEBUG_LOG_PATH, "a") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")
    except IOError as e:
        print(f"Warning: Could not write to {DEBUG_LOG_PATH}: {e} (Message: {msg})", file=sys.stderr)

# Registrar información de inicio del agente MCP
log_mcp_agent("==== Arrancando agente MCP ====")
log_mcp_agent(f"CWD: {os.getcwd()}")
log_mcp_agent(f"sys.path: {sys.path}")

# Añadir el directorio raíz al sys.path para permitir importaciones relativas
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración del servidor desde variables de entorno
HOST = os.getenv("SERVER_HOST", "localhost")
PORT = int(os.getenv("SERVER_PORT", 8000))

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    # Punto de entrada principal cuando se ejecuta el script directamente
    log.info("Arrancando FastMCP en %s:%s …", HOST, PORT)
    # Las herramientas se registran automáticamente por FastMCP al ser importadas 
    # si están decoradas con @mcp.tool en los módulos importados (client_tools, invoice_tools)
    mcp.run(
        #transport="streamable-http",  # Opción alternativa de transporte
        transport="sse",  # Server-Sent Events como mecanismo de transporte
        host=HOST,
        port=PORT,
        path="/sse",  # Ruta para la conexión SSE
        log_level="info",  # Nivel de detalle de los logs
    )

# Comando de ejemplo para ejecutar el servidor:
#  /home/david/Documents/AI/AI-Client-Agent-MCP/.venv/bin/python -m backend.server 
