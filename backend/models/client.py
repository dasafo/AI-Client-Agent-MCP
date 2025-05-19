from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)  # BaseModel for models, EmailStr for email validation, Field for field constraints
from datetime import datetime  # For date and time handling
from typing import Optional  # For optional fields


class ClientBase(BaseModel):
    """
    Base model for a client.
    Defines common fields shared by all client models.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the client (required)",
    )
    email: EmailStr = Field(
        ..., description="Valid email address of the client (required)"
    )
    phone: Optional[str] = Field(
        None,
        min_length=6,
        max_length=20,
        description="Client's phone number (optional)",
    )
    city: Optional[str] = Field(
        None, max_length=100, description="Client's city of residence (optional)"
    )


class ClientCreate(ClientBase):
    """
    Model for creating a new client.
    """

    pass  # Uniqueness and format validation will be handled in the service, not here


class ClientUpdate(BaseModel):
    """
    Model for updating an existing client.
    All fields are optional to allow partial updates.
    """

    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="New client name (optional)",
    )
    email: Optional[EmailStr] = Field(
        None, description="New email address (optional)"
    )
    phone: Optional[str] = Field(
        None,
        min_length=6,
        max_length=20,
        description="New phone number (optional)",
    )
    city: Optional[str] = Field(
        None, max_length=100, description="New city of residence (optional)"
    )


class ClientInDB(ClientBase):
    """
    Model representing a client in the database.
    Includes additional system-generated fields.
    """

    id: int = Field(
        ..., description="Unique identifier of the client in the database"
    )
    created_at: datetime = Field(
        ..., description="Record creation date and time"
    )
    updated_at: datetime = Field(
        ..., description="Last update date and time"
    )

    class Config:
        """Model config for ORM compatibility."""

        from_attributes = True  # Allows model creation from an ORM object
