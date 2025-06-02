from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr
from datetime import datetime

# Pydantic models for client management
# These models define the data structure and validation for client operations

class ClientBase(BaseModel):
    """
    Base model for clients with common fields.
    All fields are optional in the base class.
    """
    name: Optional[str] = None  # Client name
    city: Optional[str] = None  # Client city
    email: Optional[EmailStr] = None  # Client email (validated)


class ClientCreate(ClientBase):
    """
    Model for creating new clients.
    Requires name as mandatory, other fields are optional.
    """
    name: str  # Client name (required for creation)


class ClientUpdate(ClientBase):
    """
    Model for updating existing clients.
    All fields are optional to allow partial updates.
    Inherits all optional fields from ClientBase.
    """
    pass


class ClientOut(ClientBase):
    """
    Model for client data output.
    Includes all fields needed to represent a complete client.
    """
    id: int  # Unique client ID
    name: str  # Client name (always present in output)
    created_at: datetime  # Client creation date (as datetime)

    class Config:
        from_attributes = True  # pydantic v2 - allows creating the model from ORM attributes
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ClientDeleteResponse(BaseModel):
    """
    Model for the response after deleting a client.
    Includes information about the operation success and the deleted client.
    """
    success: bool  # Indicates if the operation was successful
    message: str  # Descriptive message of the result
    deleted_client: Optional[ClientOut] = None  # Data of the deleted client (if exists)
