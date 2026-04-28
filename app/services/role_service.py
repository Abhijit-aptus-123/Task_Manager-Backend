from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Role
from math import ceil
from typing import Optional
from uuid import UUID

from app.services.audit_service import log_action


# ======================
# DEFAULT PERMISSIONS
# ======================
DEFAULT_PERMISSIONS = {
    "user": {"view": False, "create": False, "update": False, "delete": False},
    "role": {"view": False, "create": False, "update": False, "delete": False},
    "task": {"view": False, "create": False, "update": False, "delete": False},

    # UPDATED
    "audit": {"view": False},
    "analytics": {
        "view": False,
        "view_all": False   # NEW
    },

    "task_scope": {
        "view_all": False,
        "create_all": False,
        "update_all": False,
        "delete_all": False
    }
}


# ======================
# CLEAN INPUT
# ======================
def clean_input_permissions(perms: dict):
    cleaned = {}

    for module, actions in perms.items():

        # AUDIT → ONLY VIEW
        if module == "audit":
            cleaned[module] = {
                "view": actions.get("view", False)
            }
            continue

        # ANALYTICS → VIEW + VIEW_ALL
        if module == "analytics":
            cleaned[module] = {
                "view": actions.get("view", False),
                "view_all": actions.get("view_all", False)
            }
            continue

        # TASK_SCOPE
        if module == "task_scope":
            cleaned[module] = {
                "view_all": actions.get("view_all", False),
                "create_all": actions.get("create_all", False),
                "update_all": actions.get("update_all", False),
                "delete_all": actions.get("delete_all", False),
            }
            continue

        cleaned[module] = actions

    return cleaned


# ======================
# NORMALIZE PERMISSIONS
# ======================
def normalize_permissions(perms: dict):
    normalized = {}

    for module, actions in perms.items():

        # AUDIT
        if module == "audit":
            normalized[module] = {
                "view": actions.get("view", False)
            }
            continue

        # ANALYTICS
        if module == "analytics":
            normalized[module] = {
                "view": actions.get("view", False),
                "view_all": actions.get("view_all", False)
            }
            continue

        # TASK_SCOPE
        if module == "task_scope":
            normalized[module] = {
                "view_all": actions.get("view_all", False),
                "create_all": actions.get("create_all", False),
                "update_all": actions.get("update_all", False),
                "delete_all": actions.get("delete_all", False),
            }
            continue

        # DEFAULT MODULES
        view = actions.get("view", False)
        create = actions.get("create", False)
        update = actions.get("update", False)
        delete = actions.get("delete", False)

        if not view:
            normalized[module] = {
                "view": False,
                "create": False,
                "update": False,
                "delete": False
            }
            continue

        normalized[module] = {
            "view": view,
            "create": create,
            "update": update,
            "delete": delete
        }

    return normalized


# ======================
# BUILD PERMISSIONS
# ======================
def build_permissions(input_permissions):

    input_dict = {
        module: action.dict()
        for module, action in input_permissions.items()
    }

    input_dict = clean_input_permissions(input_dict)
    normalized = normalize_permissions(input_dict)

    final_permissions = {}

    for module, defaults in DEFAULT_PERMISSIONS.items():
        final_permissions[module] = normalized.get(module, defaults)

    return final_permissions


# ======================
# FORMAT RESPONSE
# ======================
def format_permissions_for_response(perms: dict):
    formatted = {}

    for module, defaults in DEFAULT_PERMISSIONS.items():
        formatted[module] = perms.get(module, defaults)

    return formatted


# ======================
# CREATE ROLE
# ======================
def create_role(data, db: Session, current_user):

    existing_role = db.query(Role).filter(Role.name.ilike(data.name)).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(
        name=data.name,
        description=data.description,
        permissions=build_permissions(data.permissions)
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    log_action(db, current_user.id, "create", "role", role.id)

    role.permissions = format_permissions_for_response(role.permissions)

    return role


# ======================
# GET ROLES
# ======================
def get_roles(page: int, limit: int, db: Session, name: Optional[str] = None, description: Optional[str] = None):

    query = db.query(Role)

    if name:
        query = query.filter(Role.name.ilike(f"%{name}%"))

    if description:
        query = query.filter(Role.description.ilike(f"%{description}%"))

    total = query.count()
    total_pages = ceil(total / limit) if total > 0 else 1

    if page > total_pages:
        raise HTTPException(status_code=400, detail=f"Page exceeds total pages ({total_pages})")

    skip = (page - 1) * limit
    roles = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": total_pages,
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "permissions": format_permissions_for_response(r.permissions),
                "user_count": len(r.users)
            }
            for r in roles
        ]
    }


# ======================
# UPDATE ROLE
# ======================
def update_role(role_id: UUID, data, db: Session, current_user):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if data.name:
        role.name = data.name

    if data.description is not None:
        role.description = data.description

    if data.permissions is not None:
        role.permissions = build_permissions(data.permissions)

    db.commit()
    db.refresh(role)

    log_action(db, current_user.id, "update", "role", role.id)

    role.permissions = format_permissions_for_response(role.permissions)

    return role


# ======================
# DELETE ROLE
# ======================
def delete_role(role_id: UUID, db: Session, current_user):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.users:
        raise HTTPException(status_code=400, detail="Role assigned to users")

    db.delete(role)
    db.commit()

    log_action(db, current_user.id, "delete", "role", role_id)

    return {"message": "Role deleted"}