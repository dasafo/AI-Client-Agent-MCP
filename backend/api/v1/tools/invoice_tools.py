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
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import date

@mcp.tool(
    name="list_invoices",
    description="Listar todas las facturas de la base de datos."
)
async def list_invoices() -> Dict[str, Any]:
    try:
        invoices_data = await service_get_all_invoices()
        invoices = [InvoiceOut(**inv) for inv in invoices_data]
        print(f"TOOL list_invoices responde: {[i.model_dump() for i in invoices]}")
        return {"success": True, "invoices": [i.model_dump() for i in invoices]}
    except Exception as e:
        print(f"ERROR en list_invoices: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="get_invoice",
    description="Obtener una factura por su ID."
)
async def get_invoice(invoice_id: int) -> Dict[str, Any]:
    try:
        invoice_data = await service_get_invoice_by_id(invoice_id)
        if not invoice_data:
            return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada"}
        invoice = InvoiceOut(**invoice_data)
        print(f"TOOL get_invoice responde: {invoice.model_dump()}")
        return {"success": True, "invoice": invoice.model_dump()}
    except Exception as e:
        print(f"ERROR en get_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="list_client_invoices",
    description="Listar todas las facturas de un cliente específico."
)
async def list_client_invoices(client_id: int) -> Dict[str, Any]:
    try:
        invoices_data = await service_get_invoices_by_client_id(client_id)
        invoices = [InvoiceOut(**inv) for inv in invoices_data]
        # Podríamos verificar si el cliente existe primero, pero por ahora lo dejamos así.
        print(f"TOOL list_client_invoices responde para client_id {client_id}: {[i.model_dump() for i in invoices]}")
        return {"success": True, "invoices": [i.model_dump() for i in invoices]}
    except Exception as e:
        print(f"ERROR en list_client_invoices: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="create_invoice",
    description="Crear una nueva factura."
)
async def create_invoice_tool(
    client_id: int, 
    amount: str, # Recibimos como str para convertir a Decimal aquí
    issued_at: Optional[str] = None, # Recibimos como str para convertir a date
    due_date: Optional[str] = None, # Recibimos como str para convertir a date
    status: Optional[str] = None
) -> Dict[str, Any]:
    try:
        invoice_in = InvoiceCreate(
            client_id=client_id, 
            amount=Decimal(amount),
            issued_at=date.fromisoformat(issued_at) if issued_at else None,
            due_date=date.fromisoformat(due_date) if due_date else None,
            status=status
        )
        new_invoice_data = await service_create_invoice(invoice_in)
        new_invoice = InvoiceOut(**new_invoice_data)
        print(f"TOOL create_invoice responde: {new_invoice.model_dump()}")
        return {"success": True, "invoice": new_invoice.model_dump()}
    except Exception as e:
        print(f"ERROR en create_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="update_invoice",
    description="Actualizar una factura existente."
)
async def update_invoice_tool(
    invoice_id: int, 
    client_id: Optional[int] = None,
    amount: Optional[str] = None, 
    issued_at: Optional[str] = None, 
    due_date: Optional[str] = None, 
    status: Optional[str] = None
) -> Dict[str, Any]:
    try:
        update_data = InvoiceUpdate(
            client_id=client_id,
            amount=Decimal(amount) if amount else None,
            issued_at=date.fromisoformat(issued_at) if issued_at else None,
            due_date=date.fromisoformat(due_date) if due_date else None,
            status=status
        ).model_dump(exclude_unset=True)

        if not update_data:
            return {"success": False, "error": "No se proporcionaron datos para actualizar"}
        
        # Convertir a InvoiceUpdate Pydantic model antes de pasar al servicio
        invoice_update_pydantic = InvoiceUpdate(**update_data) 

        updated_invoice_data = await service_update_invoice(invoice_id, invoice_update_pydantic)
        if not updated_invoice_data:
            return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada o error al actualizar"}
        
        updated_invoice = InvoiceOut(**updated_invoice_data)
        print(f"TOOL update_invoice responde: {updated_invoice.model_dump()}")
        return {"success": True, "invoice": updated_invoice.model_dump()}
    except Exception as e:
        print(f"ERROR en update_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="delete_invoice",
    description="Eliminar una factura de la base de datos."
)
async def delete_invoice_tool(invoice_id: int) -> InvoiceDeleteResponse:
    try:
        invoice_to_delete = await service_get_invoice_by_id(invoice_id)
        if not invoice_to_delete:
            return InvoiceDeleteResponse(success=False, message=f"Factura con ID {invoice_id} no encontrada")
        
        deleted_invoice_out = InvoiceOut(**invoice_to_delete)
        
        deleted = await service_delete_invoice(invoice_id)
        if deleted:
            print(f"TOOL delete_invoice responde: Factura ID {invoice_id} eliminada")
            return InvoiceDeleteResponse(
                success=True, 
                message=f"Factura con ID {invoice_id} eliminada correctamente",
                deleted_invoice=deleted_invoice_out
            )
        else:
            return InvoiceDeleteResponse(success=False, message=f"No se pudo eliminar la factura con ID {invoice_id}")
    except Exception as e:
        print(f"ERROR en delete_invoice: {str(e)}")
        return InvoiceDeleteResponse(success=False, message=str(e)) 