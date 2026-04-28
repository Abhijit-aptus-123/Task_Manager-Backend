from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union
from uuid import UUID


# ======================
# BASE PERMISSION
# ======================
class BasePermission(BaseModel):
    view: bool = False
    create: bool = False
    update: bool = False
    delete: bool = False


# ======================
# TASK PERMISSION
# ======================
class TaskPermission(BasePermission):
    pass


# ======================
# TASK SCOPE
# ======================
class TaskScope(BaseModel):
    view_all: bool = False
    create_all: bool = False
    update_all: bool = False
    delete_all: bool = False


# ======================
# ANALYTICS PERMISSION  NEW
# ======================
class AnalyticsPermission(BaseModel):
    view: bool = False
    view_all: bool = False


# ======================
# CREATE ROLE
# ======================
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

    permissions: Dict[
        str,
        Union[BasePermission, TaskPermission, TaskScope, AnalyticsPermission]
    ] = Field(
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
                "create": True,
                "update": True,
                "delete": False
            },
            "audit": {
                "view": True
            },
            "analytics": {
                "view": True,
                "view_all": True   # NEW
            },
            "task_scope": {
                "view_all": True,
                "create_all": False,
                "update_all": True,
                "delete_all": False
            }
        }
    )


# ======================
# UPDATE ROLE
# ======================
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[
        Dict[str, Union[BasePermission, TaskPermission, TaskScope, AnalyticsPermission]]
    ] = None


# ======================
# RESPONSE ROLE
# ======================
class RoleResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    permissions: Dict[str, dict]
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
    offset: int
    data: List[RoleResponse]