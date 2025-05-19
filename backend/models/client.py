# Importaciones para la definición de modelos y tipos de datos
from pydantic import BaseModel, EmailStr, Field  # BaseModel para modelos, EmailStr para validación de emails, Field para restricciones de campos
from datetime import datetime  # Para manejar fechas y horas
from typing import Optional  # Para campos opcionales

class ClientBase(BaseModel):
    """
    Modelo base para un cliente.
    Define los campos comunes que comparten todos los modelos de cliente.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo del cliente (obligatorio)")
    email: EmailStr = Field(..., description="Correo electrónico válido del cliente (obligatorio)")
    phone: Optional[str] = Field(None, min_length=6, max_length=20, description="Número de teléfono del cliente (opcional)")
    city: Optional[str] = Field(None, max_length=100, description="Ciudad de residencia del cliente (opcional)")

class ClientCreate(ClientBase):
    """
    Modelo para la creación de un nuevo cliente.
    Hereda todos los campos de ClientBase sin modificaciones.
    """
    pass

class ClientUpdate(BaseModel):
    """
    Modelo para la actualización de un cliente existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nuevo nombre del cliente (opcional)")
    email: Optional[EmailStr] = Field(None, description="Nuevo correo electrónico (opcional)")
    phone: Optional[str] = Field(None, min_length=6, max_length=20, description="Nuevo número de teléfono (opcional)")
    city: Optional[str] = Field(None, max_length=100, description="Nueva ciudad de residencia (opcional)")

class ClientInDB(ClientBase):
    """
    Modelo que representa un cliente en la base de datos.
    Incluye campos adicionales generados por el sistema.
    """
    id: int = Field(..., description="Identificador único del cliente en la base de datos")
    created_at: datetime = Field(..., description="Fecha y hora de creación del registro")
    updated_at: datetime = Field(..., description="Fecha y hora de la última actualización")

    class Config:
        """Configuración del modelo para compatibilidad con ORM."""
        from_attributes = True  # Permite la creación del modelo desde un objeto ORM
