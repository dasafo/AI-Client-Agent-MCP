from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date, datetime
from decimal import Decimal

# Pydantic models for invoice management
# These models define the data structure and validation for invoice operations

class InvoiceBase(BaseModel):
    """
    Base model for invoices with common fields.
    All fields are optional in the base class.
    """
    client_id: Optional[int] = None  # ID of the client associated with the invoice
    amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)  # Invoice amount with 2 decimal places
    issued_at: Optional[date] = None  # Date when the invoice was issued
    due_date: Optional[date] = None  # Due date for payment
    status: Optional[Literal['pending', 'paid', 'canceled']] = None  # Invoice status (restricted)

class InvoiceCreate(InvoiceBase):
    """
    Model for creating new invoices.
    Requires client_id and amount as mandatory.
    """
    client_id: int  # Client ID (required for creation)
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)  # Amount (required for creation)
    # issued_at can have a default value in the database
    # status can have a default value in the database

class InvoiceUpdate(InvoiceBase):
    """
    Model for updating existing invoices.
    All fields are optional to allow partial updates.
    """
    pass

class InvoiceOut(InvoiceBase):
    """
    Model for invoice data output.
    Includes all fields needed to represent a complete invoice.
    """
    id: int  # Unique invoice ID
    client_id: int  # Ensures client_id is always present in the output
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)  # Ensures amount is always present
    issued_at: date  # Ensures issued_at is always present (has a default value in the DB)
    status: Literal['pending', 'paid', 'canceled']  # Ensures status is always present and valid

    class Config:
        from_attributes = True  # pydantic v2 - allows creating the model from ORM attributes
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            datetime: lambda v: v.isoformat() if v else None
        }

class InvoiceDeleteResponse(BaseModel):
    """
    Model for the response after deleting an invoice.
    Includes information about the operation success and the deleted invoice.
    """
    success: bool  # Indicates if the operation was successful
    message: str  # Descriptive message of the result
    deleted_invoice: Optional[InvoiceOut] = None  # Data of the deleted invoice (if exists) 