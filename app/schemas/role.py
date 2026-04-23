from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union
from uuid import UUID


# ======================
# BASE PERMISSION (NO view_all)
# ======================
class BasePermission(BaseModel):
    view: bool = False
    create: bool = False
    update: bool = False
    delete: bool = False


# ======================
# TASK PERMISSION (WITH view_all)
# ======================
class TaskPermission(BasePermission):
    view_all: bool = False   # ✅ ONLY HERE


# ======================
# CREATE ROLE
# ======================
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

    permissions: Dict[str, Union[BasePermission, TaskPermission]] = Field(
        ...,
        example={
            "user": {
                "view": True,
                "create": True,
                "update": True,
                "delete": True
            },
            "role": {
                "view": True,
                "create": True,
                "update": True,
                "delete": True
            },
            "task": {
                "view": True,
                "view_all": False,
                "create": True,
                "update": True,
                "delete": False
            }
        }
    )


# ======================
# UPDATE ROLE
# ======================
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Dict[str, Union[BasePermission, TaskPermission]]] = None


# ======================
# RESPONSE ROLE
# ======================
class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    permissions: Dict[str, dict]   # ✅ flexible output
    user_count: int = 0

    class Config:
        from_attributes = True


# ======================
# PAGINATED RESPONSE
# ======================
class PaginatedRoles(BaseModel):
    total: int
    page: int
    limit: int
    offset: int   # (your total_pages logic)
    data: List[RoleResponse]