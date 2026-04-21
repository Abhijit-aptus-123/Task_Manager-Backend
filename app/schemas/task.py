from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import UUID


# ======================
# USER (for response)
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
    if value in ["", None]:
        return None
    return value


# ======================
# CREATE TASK
# ======================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

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
    id: UUID   #  FIXED (was int )
    title: str
    description: Optional[str]

    assigned_user_id: Optional[UUID]
    assigned_user: Optional[UserInfo]

    status: Optional[str]

    class Config:
        from_attributes = True