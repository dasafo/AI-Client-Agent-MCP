from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportOut(BaseModel):
    id: int
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    period: Optional[str] = None
    manager_email: str
    manager_name: str
    report_type: str
    report_text: str
    created_at: datetime

    class Config:
        from_attributes = True 
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        } 