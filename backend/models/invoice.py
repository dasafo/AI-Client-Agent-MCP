from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

# Modelos Pydantic para la gestión de facturas
# Estos modelos definen la estructura de datos y validación para las operaciones con facturas

class InvoiceBase(BaseModel):
    """
    Modelo base para facturas con campos comunes.
    Todos los campos son opcionales en la clase base.
    """
    client_id: Optional[int] = None  # ID del cliente asociado a la factura
    amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)  # Monto de la factura con 2 decimales
    issued_at: Optional[date] = None  # Fecha de emisión de la factura
    due_date: Optional[date] = None  # Fecha de vencimiento de la factura
    status: Optional[str] = None  # Estado de la factura (pending, completed, canceled)

class InvoiceCreate(InvoiceBase):
    """
    Modelo para la creación de nuevas facturas.
    Requiere client_id y amount obligatoriamente.
    """
    client_id: int  # ID del cliente (obligatorio para crear)
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)  # Monto (obligatorio para crear)
    # issued_at puede tener un valor por defecto en la base de datos
    # status puede tener un valor por defecto en la base de datos

class InvoiceUpdate(InvoiceBase):
    """
    Modelo para actualizar facturas existentes.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    # Todos los campos son opcionales para actualización, hereda de InvoiceBase
    # Los campos específicos pueden ser opcionales si tienen valores por defecto en la BD que no deberían ser sobreescritos por None
    client_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    issued_at: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class InvoiceOut(InvoiceBase):
    """
    Modelo para la salida de datos de facturas.
    Incluye todos los campos necesarios para representar una factura completa.
    """
    id: int  # ID único de la factura
    client_id: int  # Asegura que client_id siempre esté presente en la salida
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)  # Asegura que amount siempre esté presente
    issued_at: date  # Asegura que issued_at siempre esté presente (tiene un valor por defecto en la BD)
    status: str  # Asegura que status siempre esté presente (tiene un valor por defecto en la BD)
    # due_date sigue siendo opcional

    class Config:
        # orm_mode = True # pydantic v1
        from_attributes = True  # pydantic v2 - permite crear el modelo desde atributos de un ORM

class InvoiceDeleteResponse(BaseModel):
    """
    Modelo para la respuesta tras eliminar una factura.
    Incluye información sobre el éxito de la operación y la factura eliminada.
    """
    success: bool  # Indica si la operación fue exitosa
    message: str  # Mensaje descriptivo del resultado
    deleted_invoice: Optional[InvoiceOut] = None  # Datos de la factura eliminada (si existe) 