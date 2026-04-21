from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from uuid import UUID


# ======================
# ROLE BASIC
# ======================
class RoleBasic(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


# ======================
# CREATE USER
# ======================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_ids: List[UUID]   #  CHANGED


# ======================
# LOGIN USER
# ======================
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ======================
# UPDATE USER
# ======================
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role_ids: Optional[List[UUID]] = None   #  CHANGED


# ======================
# RESPONSE USER
# ======================
class UserResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleBasic]
    status: str = "Active"

    class Config:
        from_attributes = True


# ======================
# PAGINATION
# ======================
class PaginatedUsers(BaseModel):
    total: int
    page: int
    limit: int
    offset: int
    data: List[UserResponse]


# ======================
# /auth/me
# ======================
class UserMeResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleBasic]

    class Config:
        from_attributes = True