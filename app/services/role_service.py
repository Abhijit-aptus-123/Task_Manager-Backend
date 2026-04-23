from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Role
from math import ceil
from typing import Optional
from uuid import UUID


# ======================
# DEFAULT PERMISSIONS
# ======================
DEFAULT_PERMISSIONS = {
    "user": {"view": False, "create": False, "update": False, "delete": False},
    "role": {"view": False, "create": False, "update": False, "delete": False},
    "task": {
        "view": False,
        "view_all": False,
        "create": False,
        "update": False,
        "delete": False
    },
}


# ======================
#  STRICT CLEAN INPUT
# ======================
def clean_input_permissions(perms: dict):
    cleaned = {}

    for module, actions in perms.items():

        # Remove view_all from non-task modules
        if module != "task":
            actions = {k: v for k, v in actions.items() if k != "view_all"}

        cleaned[module] = actions

    return cleaned


# ======================
# NORMALIZE
# ======================
def normalize_permissions(perms: dict):
    normalized = {}

    for module, actions in perms.items():

        view = actions.get("view", False)
        view_all = actions.get("view_all", False)
        create = actions.get("create", False)
        update = actions.get("update", False)
        delete = actions.get("delete", False)

        # Only task can have view_all
        if module != "task":
            view_all = False

        # view_all ⇒ view
        if view_all:
            view = True

        # if view = False → everything False
        if not view:
            if module == "task":
                normalized[module] = {
                    "view": False,
                    "view_all": False,
                    "create": False,
                    "update": False,
                    "delete": False
                }
            else:
                normalized[module] = {
                    "view": False,
                    "create": False,
                    "update": False,
                    "delete": False
                }
            continue

        # if any action True → view True
        if create or update or delete:
            view = True

        if module == "task":
            normalized[module] = {
                "view": view,
                "view_all": view_all,
                "create": create,
                "update": update,
                "delete": delete
            }
        else:
            normalized[module] = {
                "view": view,
                "create": create,
                "update": update,
                "delete": delete
            }

    return normalized


# ======================
# BUILD ( FULL REBUILD)
# ======================
def build_permissions(input_permissions):

    input_dict = {
        module: action.dict()
        for module, action in input_permissions.items()
    }

    #  CLEAN FIRST
    input_dict = clean_input_permissions(input_dict)

    normalized = normalize_permissions(input_dict)

    final_permissions = {}

    for module, defaults in DEFAULT_PERMISSIONS.items():
        final_permissions[module] = normalized.get(module, defaults)

    return final_permissions


# ======================
# CREATE ROLE
# ======================
def create_role(data, db: Session):

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

    return role


# ======================
# GET ROLES
# ======================
def get_roles(page, limit, db, role_id=None, name=None, description=None):

    query = db.query(Role)

    if role_id:
        query = query.filter(Role.id == role_id)

    if name:
        query = query.filter(Role.name.ilike(f"%{name}%"))

    if description:
        query = query.filter(Role.description.ilike(f"%{description}%"))

    total = query.count()
    total_pages = ceil(total / limit) if total > 0 else 1

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
                "permissions": r.permissions,
                "user_count": len(r.users)
            }
            for r in roles
        ]
    }


# ======================
# UPDATE ROLE ( FIXED)
# ======================
def update_role(role_id: UUID, data, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if data.name:
        role.name = data.name

    if data.description is not None:
        role.description = data.description

    if data.permissions is not None:
        #  FULL REBUILD (ignore old DB completely)
        role.permissions = build_permissions(data.permissions)

    db.commit()
    db.refresh(role)

    return role


# ======================
# DELETE ROLE
# ======================
def delete_role(role_id: UUID, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.users:
        raise HTTPException(status_code=400, detail="Role assigned to users")

    db.delete(role)
    db.commit()

    return {"message": "Role deleted"}