from pydantic import BaseModel
from typing import Optional


class ClientCreate(BaseModel):
    name: str
    city: Optional[str] = None
    email: Optional[str] = None


class ClientOut(ClientCreate):
    id: int
    created_at: str
