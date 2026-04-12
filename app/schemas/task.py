from pydantic import BaseModel, Field
from typing import Optional


# ======================
# USER (for response)
# ======================
class UserInfo(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


# ======================
# CREATE TASK
# ======================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    assigned_user_id: int = Field(alias="user_id")

    class Config:
        populate_by_name = True


# ======================
# UPDATE TASK
# ======================
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_user_id: Optional[int] = Field(default=None, alias="user_id")

    class Config:
        populate_by_name = True


# ======================
# RESPONSE SCHEMA
# ======================
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]

    assigned_user_id: Optional[int]
    assigned_user: Optional[UserInfo]   # 🔥 includes email

    class Config:
        from_attributes = True