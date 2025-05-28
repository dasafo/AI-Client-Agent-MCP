from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class InvoiceBase(BaseModel):
    client_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    issued_at: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    client_id: int
    amount: Decimal = Field(..., max_digits=10, decimal_places=2)
    # issued_at can default in DB or be set here
    # status can default in DB or be set here

class InvoiceUpdate(InvoiceBase):
    # All fields are optional for update, inherits from InvoiceBase
    # specific fields can be made optional if they have defaults in DB that shouldn't be overridden by None
    client_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    issued_at: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class InvoiceOut(InvoiceBase):
    id: int
    client_id: int # Ensure client_id is always present in output
    amount: Decimal = Field(..., max_digits=10, decimal_places=2) # Ensure amount is always present
    issued_at: date # Ensure issued_at is always present (as it has a DB default)
    status: str # Ensure status is always present (as it has a DB default)
    # due_date remains optional

    class Config:
        # orm_mode = True # pydantic v1
        from_attributes = True # pydantic v2

class InvoiceDeleteResponse(BaseModel):
    success: bool
    message: str
    deleted_invoice: Optional[InvoiceOut] = None 