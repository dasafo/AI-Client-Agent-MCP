from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)  # BaseModel para modelos, EmailStr para validación de email, Field para restricciones de campos
from datetime import datetime  # Para manejo de fechas y horas
from typing import Optional  # Para campos opcionales


class ClientBase(BaseModel):
    """
    Modelo base para un cliente.
    Define los campos comunes compartidos por todos los modelos de cliente.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del cliente (obligatorio)",
    )
    email: EmailStr = Field(
        ..., description="Dirección de correo electrónico válida del cliente (obligatorio)"
    )
    phone: Optional[str] = Field(
        None,
        min_length=6,
        max_length=20,
        description="Número de teléfono del cliente (opcional)",
    )
    city: Optional[str] = Field(
        None, max_length=100, description="Ciudad de residencia del cliente (opcional)"
    )


class ClientCreate(ClientBase):
    """
    Modelo para la creación de un nuevo cliente.
    Hereda todos los campos del modelo base.
    """

    pass  # Modelo para crear un nuevo cliente. No se requiere implementación adicional.


class ClientUpdate(BaseModel):
    """
    Modelo para actualizar un cliente existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """

    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nuevo nombre del cliente (opcional)",
    )
    email: Optional[EmailStr] = Field(None, description="Nuevo correo electrónico (opcional)")
    phone: Optional[str] = Field(
        None,
        min_length=6,
        max_length=20,
        description="Nuevo número de teléfono (opcional)",
    )
    city: Optional[str] = Field(
        None, max_length=100, description="Nueva ciudad de residencia (opcional)"
    )


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

        from_attributes = True  # Permite la creación del modelo a partir de un objeto ORM
