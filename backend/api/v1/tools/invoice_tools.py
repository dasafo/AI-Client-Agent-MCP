from backend.mcp_instance import mcp
from backend.services.invoice_service import (
    get_all_invoices as service_get_all_invoices,
    get_invoice_by_id as service_get_invoice_by_id,
    get_invoices_by_client_id as service_get_invoices_by_client_id,
    create_invoice as service_create_invoice,
    update_invoice as service_update_invoice,
    delete_invoice as service_delete_invoice
)
from backend.models.invoice import (
    InvoiceCreate, 
    InvoiceUpdate, 
    InvoiceOut, 
    InvoiceDeleteResponse
)
from typing import List, Dict, Any
from decimal import Decimal
from datetime import date

# Herramientas para la gestión de facturas
# Estas funciones exponen la funcionalidad de gestión de facturas a través del MCP (Master Control Program)

@mcp.tool(
    name="list_invoices",
    description="Listar todas las facturas de la base de datos."
)
async def list_invoices() -> Dict[str, Any]:
    invoices_data = await service_get_all_invoices()
    if isinstance(invoices_data, dict) and not invoices_data.get("success", True):
        return invoices_data
    invoices = [InvoiceOut(**inv) for inv in invoices_data]
    return {"success": True, "invoices": [i.model_dump() for i in invoices]}

@mcp.tool(
    name="get_invoice",
    description="Obtener una factura por su ID."
)
async def get_invoice(invoice_id: int) -> Dict[str, Any]:
    invoice_data = await service_get_invoice_by_id(invoice_id)
    if not invoice_data:
        return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada"}
    if isinstance(invoice_data, dict) and not invoice_data.get("success", True):
        return invoice_data
    invoice = InvoiceOut(**invoice_data)
    return {"success": True, "invoice": invoice.model_dump()}

@mcp.tool(
    name="list_client_invoices",
    description="Listar todas las facturas de un cliente específico."
)
async def list_client_invoices(client_id: int) -> Dict[str, Any]:
    invoices_data = await service_get_invoices_by_client_id(client_id)
    if isinstance(invoices_data, dict) and not invoices_data.get("success", True):
        return invoices_data
    invoices = [InvoiceOut(**inv) for inv in invoices_data]
    return {"success": True, "invoices": [i.model_dump() for i in invoices]}

@mcp.tool(
    name="create_invoice",
    description="Crear una nueva factura."
)
async def create_invoice_tool(
    client_id: int, 
    amount: str, 
    issued_at: str = "", 
    due_date: str = "", 
    status: str = ""
) -> Dict[str, Any]:
    invoice_in = InvoiceCreate(
        client_id=client_id, 
        amount=Decimal(amount),
        issued_at=date.fromisoformat(issued_at) if issued_at else None,
        due_date=date.fromisoformat(due_date) if due_date else None,
        status=status if status else None
    )
    new_invoice_data = await service_create_invoice(invoice_in)
    if isinstance(new_invoice_data, dict) and not new_invoice_data.get("success", True):
        return new_invoice_data
    new_invoice = InvoiceOut(**new_invoice_data)
    return {"success": True, "invoice": new_invoice.model_dump()}

@mcp.tool(
    name="update_invoice",
    description="Actualizar una factura existente."
)
async def update_invoice_tool(
    invoice_id: int, 
    client_id: str = "",
    amount: str = "", 
    issued_at: str = "", 
    due_date: str = "", 
    status: str = ""
) -> Dict[str, Any]:
    update_payload = {}
    if client_id:
        update_payload['client_id'] = int(client_id)
    if amount:
        update_payload['amount'] = Decimal(amount)
    if issued_at:
        update_payload['issued_at'] = date.fromisoformat(issued_at)
    if due_date:
        update_payload['due_date'] = date.fromisoformat(due_date)
    if status:
        update_payload['status'] = status
    if not update_payload:
        return {"success": False, "error": "No se proporcionaron datos para actualizar"}
    invoice_update_pydantic = InvoiceUpdate(**update_payload)
    updated_invoice_data = await service_update_invoice(invoice_id, invoice_update_pydantic)
    if not updated_invoice_data:
        return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada o error al actualizar"}
    if isinstance(updated_invoice_data, dict) and not updated_invoice_data.get("success", True):
        return updated_invoice_data
    updated_invoice = InvoiceOut(**updated_invoice_data)
    return {"success": True, "invoice": updated_invoice.model_dump()}

@mcp.tool(
    name="delete_invoice",
    description="Eliminar una factura de la base de datos."
)
async def delete_invoice_tool(invoice_id: int) -> InvoiceDeleteResponse:
    invoice_to_delete = await service_get_invoice_by_id(invoice_id)
    if not invoice_to_delete:
        return InvoiceDeleteResponse(success=False, message=f"Factura con ID {invoice_id} no encontrada")
    if isinstance(invoice_to_delete, dict) and not invoice_to_delete.get("success", True):
        return InvoiceDeleteResponse(success=False, message=invoice_to_delete.get("error", "Error desconocido"))
    deleted_invoice_out = InvoiceOut(**invoice_to_delete)
    deleted = await service_delete_invoice(invoice_id)
    if deleted:
        return InvoiceDeleteResponse(
            success=True, 
            message=f"Factura con ID {invoice_id} eliminada correctamente",
            deleted_invoice=deleted_invoice_out
        )
    else:
        return InvoiceDeleteResponse(success=False, message=f"No se pudo eliminar la factura con ID {invoice_id}") 