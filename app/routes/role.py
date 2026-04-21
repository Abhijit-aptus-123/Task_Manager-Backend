from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
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
    return create_role(data, db)


# ======================
# GET ROLES (FILTER + PAGINATION)
# ======================
@router.get("/", response_model=PaginatedRoles)
def read(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    name: Optional[str] = Query(None),
    role_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "view"))
):
    return get_roles(page, limit, db, name, role_id)


# ======================
# UPDATE ROLE
# ======================
@router.put("/{role_id}", response_model=RoleResponse)
def update(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "update"))
):
    return update_role(role_id, data, db)


# ======================
# DELETE ROLE
# ======================
@router.delete("/{role_id}")
def delete(
    role_id: int,
    db: Session = Depends(get_db),
    user=Depends(check_permission("role", "delete"))
):
    return delete_role(role_id, db)