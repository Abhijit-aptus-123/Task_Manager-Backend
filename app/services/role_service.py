from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Role, User


# ======================
#  DEFAULT MODULES
# ======================
DEFAULT_PERMISSIONS = {
    "dashboard": {"view": False, "create": False, "update": False, "delete": False},
    "user": {"view": False, "create": False, "update": False, "delete": False},
    "role": {"view": False, "create": False, "update": False, "delete": False},
    "task": {"view": False, "create": False, "update": False, "delete": False},
}


# ======================
#  NORMALIZE PERMISSIONS (MASTER LOGIC)
# ======================
def normalize_permissions(perms: dict):
    """
    Rules:
    1. If view = False → everything False
    2. If any action True → view = True
    """

    normalized = {}

    for module, actions in perms.items():

        view = actions.get("view", False)
        create = actions.get("create", False)
        update = actions.get("update", False)
        delete = actions.get("delete", False)

        #  RULE 1: view = False → everything False
        if not view:
            normalized[module] = {
                "view": False,
                "create": False,
                "update": False,
                "delete": False
            }
            continue

        # RULE 2: any action → view = True
        if create or update or delete:
            view = True

        normalized[module] = {
            "view": view,
            "create": create,
            "update": update,
            "delete": delete
        }

    return normalized


# ======================
#  BUILD FINAL PERMISSIONS
# ======================
def build_permissions(input_permissions):
    final_permissions = {}

    # Convert Pydantic → dict
    input_dict = {
        module: action.dict()
        for module, action in input_permissions.items()
    }

    # Apply normalization first
    normalized = normalize_permissions(input_dict)

    # Merge with defaults
    for module, defaults in DEFAULT_PERMISSIONS.items():
        if module in normalized:
            final_permissions[module] = normalized[module]
        else:
            final_permissions[module] = defaults

    return final_permissions


# ======================
# CREATE ROLE
# ======================
def create_role(data, db: Session):

    existing_role = db.query(Role).filter(Role.name.ilike(data.name)).first()
    if existing_role:
        raise HTTPException(
            status_code=400,
            detail=f"Role '{data.name}' already exists"
        )

    permissions_dict = build_permissions(data.permissions)

    role = Role(
        name=data.name,
        description=data.description,
        permissions=permissions_dict
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


# ======================
# GET ROLES (FILTER + PAGINATION)
# ======================
def get_roles(page: int, limit: int, db: Session, name=None, role_id=None):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination values")

    query = db.query(Role)

    #  FILTER BY ID
    if role_id:
        query = query.filter(Role.id == role_id)

    #  FILTER BY NAME (PARTIAL SEARCH)
    if name:
        query = query.filter(Role.name.ilike(f"%{name}%"))

    total = query.count()

    offset = (page - 1) * limit

    roles = query.offset(offset).limit(limit).all()

    result = []
    for role in roles:
        result.append({
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": role.permissions,
            "user_count": len(role.users)
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": offset,
        "data": result
    }

# ======================
# UPDATE ROLE
# ======================
def update_role(role_id, data, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    #  Duplicate check
    if data.name:
        existing_role = (
            db.query(Role)
            .filter(Role.name.ilike(data.name))
            .filter(Role.id != role_id)
            .first()
        )

        if existing_role:
            raise HTTPException(
                status_code=400,
                detail=f"Role '{data.name}' already exists"
            )

        role.name = data.name

    if data.description is not None:
        role.description = data.description

    if data.permissions is not None:
        role.permissions = build_permissions(data.permissions)

    db.commit()
    db.refresh(role)

    return role


# ======================
# DELETE ROLE
# ======================
def delete_role(role_id, db: Session):

    role = db.query(Role).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    #  FIX: many-to-many check
    if role.users:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete role assigned to users"
        )

    db.delete(role)
    db.commit()

    return {"message": "Role deleted successfully"}