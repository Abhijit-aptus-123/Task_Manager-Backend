from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from app.db.models import User, Role


# ======================
# GET USERS (MULTI-ROLE FILTER)
# ======================
def get_users_paginated(
    page: int,
    limit: int,
    db: Session,
    email: str = None,
    roles: str = None   # comma-separated role names (for filtering)
):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination values")

    query = db.query(User)

    # 🔍 FILTER BY EMAIL
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    # 🔍 MULTI-ROLE FILTER (BY ROLE NAME)
    if roles:
        role_list = [r.strip() for r in roles.split(",")]

        query = (
            query
            .join(User.roles)
            .filter(Role.name.in_(role_list))
            .distinct()
        )

    total = query.count()

    offset = (page - 1) * limit

    users = query.offset(offset).limit(limit).all()

    result = [
        {
            "id": user.id,
            "email": user.email,
            "roles": [
                {
                    "id": role.id,
                    "name": role.name
                }
                for role in user.roles
            ],
            "status": "Active"
        }
        for user in users
    ]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": offset,
        "data": result
    }


# ======================
# UPDATE USER (ROLE_ID BASED ✅)
# ======================
def update_user(user_id: UUID, data, db: Session):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ UPDATE EMAIL
    if data.email:
        user.email = data.email

    # ✅ UPDATE ROLES USING ROLE_IDS
    if data.role_ids is not None:

        # Allow clearing roles if empty list is passed
        if len(data.role_ids) == 0:
            user.roles = []
        else:
            role_objs = db.query(Role).filter(Role.id.in_(data.role_ids)).all()

            if len(role_objs) != len(data.role_ids):
                raise HTTPException(status_code=400, detail="Invalid role IDs")

            user.roles = role_objs

    db.commit()
    db.refresh(user)

    return {
        "message": "User updated successfully",
        "user_id": user.id
    }


# ======================
# DELETE USER
# ======================
def delete_user(user_id: UUID, current_user: User, db: Session):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ❌ Prevent self delete
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}