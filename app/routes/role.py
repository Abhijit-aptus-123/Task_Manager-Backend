from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.db.database import get_db
from app.db.models import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, PaginatedRoles
from app.services.role_service import (
    create_role,
    get_roles,
    update_role,
    delete_role
)

from app.core.permission import check_permission

router = APIRouter(prefix="/roles")


# ======================
# CREATE ROLE
# ======================
@router.post("/", response_model=RoleResponse)
def create(
    data: RoleCreate,
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "create"))
):
    return create_role(data, db, user)


# ======================
# GET ROLES
# ======================
@router.get("/", response_model=PaginatedRoles)
def read(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "view"))
):
    return get_roles(page, limit, db, name, description)


# ======================
# UPDATE ROLE
# ======================
@router.put("/{role_id}", response_model=RoleResponse)
def update(
    role_id: UUID,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "update"))
):
    # FIX: pass user
    return update_role(role_id, data, db, user)


# ======================
# DELETE ROLE
# ======================
@router.delete("/{role_id}")
def delete(
    role_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "delete"))
):
    # FIX: pass user
    return delete_role(role_id, db, user)


# ======================
# GET ALL ROLES (NO PERMISSION CHECK)
# ======================
@router.get("/all")
def get_all_roles_unrestricted(
    db: Session = Depends(get_db)
):
    roles = db.query(Role).all()

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": role.permissions,
            "user_count": len(role.users)
        }
        for role in roles
    ]