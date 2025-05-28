from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClientBase(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None


class ClientCreate(ClientBase):
    name: str


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    name: str
    created_at: str

    class Config:
        from_attributes = True


class ClientDeleteResponse(BaseModel):
    success: bool
    message: str
    deleted_client: Optional[ClientOut] = None
