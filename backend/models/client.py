from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelos Pydantic para la gestión de clientes
# Estos modelos definen la estructura de datos y validación para las operaciones con clientes

class ClientBase(BaseModel):
    """
    Modelo base para clientes con campos comunes.
    Todos los campos son opcionales en la clase base.
    """
    name: Optional[str] = None  # Nombre del cliente
    city: Optional[str] = None  # Ciudad del cliente
    email: Optional[str] = None  # Email del cliente


class ClientCreate(ClientBase):
    """
    Modelo para la creación de nuevos clientes.
    Requiere name obligatoriamente, los demás campos son opcionales.
    """
    name: str  # Nombre del cliente (obligatorio para crear)


class ClientUpdate(ClientBase):
    """
    Modelo para actualizar clientes existentes.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    Hereda todos los campos opcionales de ClientBase.
    """
    pass


class ClientOut(ClientBase):
    """
    Modelo para la salida de datos de clientes.
    Incluye todos los campos necesarios para representar un cliente completo.
    """
    id: int  # ID único del cliente
    name: str  # Nombre del cliente (siempre presente en la salida)
    created_at: str  # Fecha de creación del cliente (en formato ISO)

    class Config:
        from_attributes = True  # pydantic v2 - permite crear el modelo desde atributos de un ORM


class ClientDeleteResponse(BaseModel):
    """
    Modelo para la respuesta tras eliminar un cliente.
    Incluye información sobre el éxito de la operación y el cliente eliminado.
    """
    success: bool  # Indica si la operación fue exitosa
    message: str  # Mensaje descriptivo del resultado
    deleted_client: Optional[ClientOut] = None  # Datos del cliente eliminado (si existe)
