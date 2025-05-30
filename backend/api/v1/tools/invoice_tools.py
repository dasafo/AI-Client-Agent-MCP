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
    try:
        # Obtiene todas las facturas desde el servicio
        invoices_data = await service_get_all_invoices()
        
        # Convierte los datos en objetos Pydantic para validación y serialización
        invoices = [InvoiceOut(**inv) for inv in invoices_data]
        print(f"TOOL list_invoices responde: {[i.model_dump() for i in invoices]}")
        
        # Devuelve la lista de facturas serializada
        return {"success": True, "invoices": [i.model_dump() for i in invoices]}
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en list_invoices: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="get_invoice",
    description="Obtener una factura por su ID."
)
async def get_invoice(invoice_id: int) -> Dict[str, Any]:
    try:
        # Busca la factura por su ID utilizando el servicio
        invoice_data = await service_get_invoice_by_id(invoice_id)
        if not invoice_data:
            # Si no se encuentra la factura, devuelve un mensaje de error
            return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada"}
        
        # Crea un objeto Pydantic para validación y serialización
        invoice = InvoiceOut(**invoice_data)
        print(f"TOOL get_invoice responde: {invoice.model_dump()}")
        
        # Devuelve la factura serializada
        return {"success": True, "invoice": invoice.model_dump()}
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en get_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="list_client_invoices",
    description="Listar todas las facturas de un cliente específico."
)
async def list_client_invoices(client_id: int) -> Dict[str, Any]:
    try:
        # Obtiene todas las facturas del cliente desde el servicio
        invoices_data = await service_get_invoices_by_client_id(client_id)
        
        # Convierte los datos en objetos Pydantic para validación y serialización
        invoices = [InvoiceOut(**inv) for inv in invoices_data]
        # Podríamos verificar si el cliente existe primero, pero por ahora lo dejamos así.
        print(f"TOOL list_client_invoices responde para client_id {client_id}: {[i.model_dump() for i in invoices]}")
        
        # Devuelve la lista de facturas del cliente serializada
        return {"success": True, "invoices": [i.model_dump() for i in invoices]}
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en list_client_invoices: {str(e)}")
        return {"success": False, "error": str(e)}

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
    try:
        # Crea un modelo Pydantic para validar los datos de entrada
        # Convierte tipos de datos según sea necesario (Decimal para amount, date para fechas)
        invoice_in = InvoiceCreate(
            client_id=client_id, 
            amount=Decimal(amount),
            issued_at=date.fromisoformat(issued_at) if issued_at else None,
            due_date=date.fromisoformat(due_date) if due_date else None,
            status=status if status else None
        )
        
        # Llama al servicio para crear la factura en la base de datos
        new_invoice_data = await service_create_invoice(invoice_in)
        
        # Crea un objeto Pydantic para validación y serialización de la respuesta
        new_invoice = InvoiceOut(**new_invoice_data)
        print(f"TOOL create_invoice responde: {new_invoice.model_dump()}")
        
        # Devuelve la nueva factura serializada
        return {"success": True, "invoice": new_invoice.model_dump()}
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en create_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

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
    try:
        # Prepara un diccionario con los campos a actualizar, ignorando campos vacíos
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

        # Verifica que haya al menos un campo para actualizar
        if not update_payload:
            return {"success": False, "error": "No se proporcionaron datos para actualizar"}
        
        # Crea un modelo Pydantic para validar los datos de actualización
        invoice_update_pydantic = InvoiceUpdate(**update_payload) 

        # Llama al servicio para actualizar la factura en la base de datos
        updated_invoice_data = await service_update_invoice(invoice_id, invoice_update_pydantic)
        if not updated_invoice_data:
            # Si no se encuentra la factura o hay error al actualizar, devuelve un mensaje
            return {"success": False, "error": f"Factura con ID {invoice_id} no encontrada o error al actualizar"}
        
        # Crea un objeto Pydantic para validación y serialización de la respuesta
        updated_invoice = InvoiceOut(**updated_invoice_data)
        print(f"TOOL update_invoice responde: {updated_invoice.model_dump()}")
        
        # Devuelve la factura actualizada serializada
        return {"success": True, "invoice": updated_invoice.model_dump()}
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en update_invoice: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="delete_invoice",
    description="Eliminar una factura de la base de datos."
)
async def delete_invoice_tool(invoice_id: int) -> InvoiceDeleteResponse:
    try:
        # Primero verifica que la factura exista
        invoice_to_delete = await service_get_invoice_by_id(invoice_id)
        if not invoice_to_delete:
            # Si no se encuentra la factura, devuelve un mensaje de error
            return InvoiceDeleteResponse(success=False, message=f"Factura con ID {invoice_id} no encontrada")
        
        # Crea un objeto Pydantic para la factura que se va a eliminar
        deleted_invoice_out = InvoiceOut(**invoice_to_delete)
        
        # Llama al servicio para eliminar la factura de la base de datos
        deleted = await service_delete_invoice(invoice_id)
        if deleted:
            # Si se eliminó correctamente, devuelve un mensaje de éxito y los datos de la factura eliminada
            print(f"TOOL delete_invoice responde: Factura ID {invoice_id} eliminada")
            return InvoiceDeleteResponse(
                success=True, 
                message=f"Factura con ID {invoice_id} eliminada correctamente",
                deleted_invoice=deleted_invoice_out
            )
        else:
            # Si hubo un problema al eliminar, devuelve un mensaje de error
            return InvoiceDeleteResponse(success=False, message=f"No se pudo eliminar la factura con ID {invoice_id}")
    except Exception as e:
        # Captura cualquier error, lo registra y lo devuelve en la respuesta
        print(f"ERROR en delete_invoice: {str(e)}")
        return InvoiceDeleteResponse(success=False, message=str(e)) 