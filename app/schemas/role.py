from pydantic import BaseModel, Field
from typing import Dict, Optional
from typing import List

# ======================
# PERMISSION STRUCTURE
# ======================
class PermissionAction(BaseModel):
    view: bool = False
    create: bool = False
    update: bool = False
    delete: bool = False


# ======================
# CREATE ROLE
# ======================
class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

    permissions: Dict[str, PermissionAction] = Field(
        ...,
        example={
            "dashboard": {
                "view": True,
                "create": False,
                "update": False,
                "delete": False
            },
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
            "task": {   # ✅ ADDED
                "view": True,
                "create": True,
                "update": True,
                "delete": True
            }
        }
    )


# ======================
# UPDATE ROLE
# ======================
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Dict[str, PermissionAction]] = None


# ======================
# RESPONSE ROLE
# ======================
class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: Dict[str, PermissionAction]
    user_count: int = 0   # ✅ DEFAULT FIX

    class Config:
        from_attributes = True

# ======================
# PAGINATED RESPONSE
# ======================
class PaginatedRoles(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    data: List[RoleResponse]