from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClientNoteCreate(BaseModel):
    client_id: int = Field(..., description="ID del cliente asociado")
    note: str = Field(
        ..., min_length=1, max_length=1000, description="Texto de la nota"
    )


class ClientNoteInDB(ClientNoteCreate):
    id: int = Field(..., description="ID único de la nota")
    created_at: datetime = Field(..., description="Fecha de creación de la nota")

    class Config:
        from_attributes = True
