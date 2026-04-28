from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AuditLogResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    resource: str
    resource_id: Optional[str]
    timestamp: str

    class Config:
        from_attributes = True