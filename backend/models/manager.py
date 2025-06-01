from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ManagerBase(BaseModel):
    name: str
    email: str
    role: Optional[str] = None

class ManagerCreate(ManagerBase):
    pass

class ManagerOut(ManagerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
