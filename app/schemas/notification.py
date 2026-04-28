from pydantic import BaseModel
from uuid import UUID

class NotificationResponse(BaseModel):
    id: UUID
    user_id: UUID
    message: str
    is_read: str
    timestamp: str

    class Config:
        from_attributes = True