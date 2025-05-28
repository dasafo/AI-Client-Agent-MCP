from backend.mcp_instance import mcp
from backend.services.client_service import get_all_clients


@mcp.tool(
    name="list_clients",
    description="Listar clientes de la base de datos",
)
async def list_clients():
    try:
        clients = await get_all_clients()  # Ya es lista de dicts
        print("TOOL list_clients responde:", clients)  # (opcional, para debug)
        return {"success": True, "clients": clients}
    except Exception as e:
        print("ERROR en list_clients:", str(e))  # (opcional, para debug)
        return {"success": False, "error": str(e)}
