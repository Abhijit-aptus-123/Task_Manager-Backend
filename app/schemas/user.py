from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from uuid import UUID


# ======================
# ROLE INFO
# ======================
class RoleInfo(BaseModel):
    id: int
    name: str
    permissions: Dict[str, Any]

    class Config:
        from_attributes = True


# ======================
# CREATE
# ======================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    roles: List[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    roles: Optional[List[str]] = None


# ======================
# RESPONSE USER
# ======================
class UserResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleInfo]
    status: str

    class Config:
        from_attributes = True


# ======================
# PAGINATION
# ======================
class PaginatedUsers(BaseModel):
    total: int
    page: int
    limit: int
    data: List[UserResponse]


# ======================
# /auth/me RESPONSE
# ======================
class UserMeResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleInfo]

    class Config:
        from_attributes = True