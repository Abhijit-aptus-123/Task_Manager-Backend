from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from uuid import UUID


# ======================
# ROLE BASIC (NO PERMISSIONS)
# ======================
class RoleBasic(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True


# ======================
# CREATE USER (ROLE IDs)
# ======================
class UserCreate(BaseModel):
    email: EmailStr
    password: str

    # Optional → handled in service (first admin or validation)
    role_ids: Optional[List[UUID]] = Field(
        default=None,
        description="List of role UUIDs"
    )


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

    role_ids: Optional[List[UUID]] = Field(
        default=None,
        description="Update roles using role UUIDs"
    )


# ======================
# USER RESPONSE (LIST)
# ======================
class UserResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleBasic]
    status: str = "Active"

    class Config:
        from_attributes = True


# ======================
# PAGINATED USERS
# ======================
class PaginatedUsers(BaseModel):
    total: int
    page: int
    limit: int
    offset: int   # represents total_pages (as per your requirement)
    data: List[UserResponse]


# ======================
# /auth/me RESPONSE
# ======================
class UserMeResponse(BaseModel):
    id: UUID
    email: str
    roles: List[RoleBasic]

    # merged permissions from all roles
    permissions: Dict[str, Any]

    class Config:
        from_attributes = True