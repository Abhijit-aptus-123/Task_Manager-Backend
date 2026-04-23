from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID


# ======================
# USER (FOR RESPONSE)
# ======================
class UserInfo(BaseModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True


# ======================
# HELPER
# ======================
def clean_user_id(value):
    if value is None:
        return None

    if isinstance(value, str) and value.strip() == "":
        return None

    return value


# ======================
# CREATE TASK
# ======================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

    #  Accept "user_id" from frontend
    assigned_user_id: Optional[UUID] = Field(
        default=None,
        alias="user_id"
    )

    status: Optional[str] = "todo"

    @field_validator("assigned_user_id", mode="before")
    @classmethod
    def validate_user_id(cls, v):
        return clean_user_id(v)

    class Config:
        populate_by_name = True


# ======================
# UPDATE TASK
# ======================
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    assigned_user_id: Optional[UUID] = Field(
        default=None,
        alias="user_id"
    )

    status: Optional[str] = None

    @field_validator("assigned_user_id", mode="before")
    @classmethod
    def validate_user_id(cls, v):
        return clean_user_id(v)

    class Config:
        populate_by_name = True


# ======================
# RESPONSE
# ======================
class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None

    assigned_user_id: Optional[UUID] = None
    assigned_user: Optional[UserInfo] = None

    status: Optional[str] = None

    class Config:
        from_attributes = True