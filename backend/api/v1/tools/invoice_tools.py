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
from backend.services.client_service import get_client_by_id as service_get_client_by_id
from typing import List, Dict, Any
from decimal import Decimal
from datetime import date
from backend.core.logging import get_logger

logger = get_logger(__name__)

# Herramientas para la gestión de facturas
# Estas funciones exponen la funcionalidad de gestión de facturas a través del MCP (Master Control Program)

@mcp.tool(
    name="list_invoices",
    description="Listar todas las facturas de la base de datos."
)
async def list_invoices() -> Dict[str, Any]:
    invoices_data = await service_get_all_invoices()
    if isinstance(invoices_data, dict) and not invoices_data.get("success", True):
        logger.error(f"Error al listar facturas: {invoices_data.get('error', invoices_data)}")
        return invoices_data
    processed_invoices = []
    for invoice_dict in invoices_data:
        processed_invoices.append(InvoiceOut(**invoice_dict))
    logger.debug(f"TOOL list_invoices responde: {[i.model_dump() for i in processed_invoices]}")
    return {"success": True, "invoices": [i.model_dump() for i in processed_invoices]}

@mcp.tool(
    name="get_invoice",
    description="Obtener una factura por su ID."
)
async def get_invoice(invoice_id: int) -> Dict[str, Any]:
    invoice_data = await service_get_invoice_by_id(invoice_id)
    if not invoice_data:
        logger.warning(f"Factura con ID {invoice_id} no encontrada")
        return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada"}
    if isinstance(invoice_data, dict) and not invoice_data.get("success", True):
        logger.error(f"Error al obtener factura: {invoice_data.get('error', invoice_data)}")
        return invoice_data
    invoice = InvoiceOut(**invoice_data)
    logger.debug(f"TOOL get_invoice responde: {invoice.model_dump()}")
    return {"success": True, "invoice": invoice.model_dump()}

@mcp.tool(
    name="list_client_invoices",
    description="Listar todas las facturas de un cliente específico."
)
async def list_client_invoices(client_id: int) -> Dict[str, Any]:
    # Validar existencia del cliente
    client = await service_get_client_by_id(client_id)
    if not client:
        logger.warning(f"Cliente con ID {client_id} no encontrado al listar facturas")
        return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
    invoices_data = await service_get_invoices_by_client_id(client_id)
    if isinstance(invoices_data, dict) and not invoices_data.get("success", True):
        logger.error(f"Error al listar facturas del cliente {client_id}: {invoices_data.get('error', invoices_data)}")
        return invoices_data
    processed_invoices = []
    for invoice_dict in invoices_data:
        processed_invoices.append(InvoiceOut(**invoice_dict))
    logger.debug(f"TOOL list_client_invoices responde para client_id {client_id}: {[i.model_dump() for i in processed_invoices]}")
    return {"success": True, "invoices": [i.model_dump() for i in processed_invoices]}

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
    # Validar existencia del cliente
    client = await service_get_client_by_id(client_id)
    if not client:
        logger.warning(f"Cliente con ID {client_id} no encontrado al crear factura")
        return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
    invoice_in = InvoiceCreate(
        client_id=client_id, 
        amount=Decimal(amount),
        issued_at=date.fromisoformat(issued_at) if issued_at else None,
        due_date=date.fromisoformat(due_date) if due_date else None,
        status=status if status else None
    )
    new_invoice_data = await service_create_invoice(invoice_in)
    if isinstance(new_invoice_data, dict) and not new_invoice_data.get("success", True):
        logger.error(f"Error al crear factura: {new_invoice_data.get('error', new_invoice_data)}")
        return new_invoice_data
    new_invoice = InvoiceOut(**new_invoice_data)
    logger.info(f"TOOL create_invoice responde: {new_invoice.model_dump()}")
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
        # Validar existencia del cliente
        client = await service_get_client_by_id(int(client_id))
        if not client:
            logger.warning(f"Cliente con ID {client_id} no encontrado al actualizar factura")
            return {"success": False, "error": f"Cliente con ID {client_id} no encontrado"}
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
        logger.warning("No se proporcionaron datos para actualizar en update_invoice_tool")
        return {"success": False, "error": "No se proporcionaron datos para actualizar"}
    invoice_update_pydantic = InvoiceUpdate(**update_payload)
    updated_invoice_data = await service_update_invoice(invoice_id, invoice_update_pydantic)
    if not updated_invoice_data:
        logger.warning(f"Factura con ID {invoice_id} no encontrada o error al actualizar")
        return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada o error al actualizar"}
    if isinstance(updated_invoice_data, dict) and not updated_invoice_data.get("success", True):
        logger.error(f"Error al actualizar factura: {updated_invoice_data.get('error', updated_invoice_data)}")
        return updated_invoice_data
    updated_invoice = InvoiceOut(**updated_invoice_data)
    logger.info(f"TOOL update_invoice responde: {updated_invoice.model_dump()}")
    return {"success": True, "invoice": updated_invoice.model_dump()}

@mcp.tool(
    name="delete_invoice",
    description="Eliminar una factura de la base de datos."
)
async def delete_invoice_tool(invoice_id: int) -> InvoiceDeleteResponse:
    invoice_to_delete = await service_get_invoice_by_id(invoice_id)
    if not invoice_to_delete:
        logger.warning(f"Factura con ID {invoice_id} no encontrada para eliminar")
        return InvoiceDeleteResponse(success=False, message=f"Factura con ID {invoice_id} no encontrada")
    if isinstance(invoice_to_delete, dict) and not invoice_to_delete.get("success", True):
        logger.error(f"Error al obtener factura para eliminar: {invoice_to_delete.get('error', invoice_to_delete)}")
        return InvoiceDeleteResponse(success=False, message=invoice_to_delete.get("error", "Error desconocido"))
    deleted_invoice_out = InvoiceOut(**invoice_to_delete)
    deleted = await service_delete_invoice(invoice_id)
    if deleted:
        logger.info(f"TOOL delete_invoice responde: Factura ID {invoice_id} eliminada")
        return InvoiceDeleteResponse(
            success=True, 
            message=f"Factura con ID {invoice_id} eliminada correctamente",
            deleted_invoice=deleted_invoice_out
        )
    else:
        logger.error(f"No se pudo eliminar la factura con ID {invoice_id}")
        return InvoiceDeleteResponse(success=False, message=f"No se pudo eliminar la factura con ID {invoice_id}") 