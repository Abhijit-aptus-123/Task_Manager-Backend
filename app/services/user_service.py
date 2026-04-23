from sqlalchemy.orm import Session
from sqlalchemy import func   # ✅ FIXED
from fastapi import HTTPException
from uuid import UUID
from typing import Optional
from math import ceil

from app.db.models import User, Role


# ======================
# GET USERS (EMAIL + MULTI ROLE FILTER - AND LOGIC)
# ======================
def get_users_paginated(
    page: int,
    limit: int,
    db: Session,
    email: Optional[str] = None,
    roles: Optional[str] = None
):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination values")

    query = db.query(User)

    # 🔍 FILTER BY EMAIL
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    #  MULTI-ROLE FILTER (AND LOGIC)
    if roles:
        role_list = [r.strip() for r in roles.split(",") if r.strip()]

        if not role_list:
            raise HTTPException(status_code=400, detail="Invalid roles input")

        query = (
            query
            .join(User.roles)
            .filter(Role.name.in_(role_list))
            .group_by(User.id)
            .having(func.count(Role.id) == len(role_list))  # ✅ AND logic
        )

    total = query.count()

    total_pages = ceil(total / limit) if total > 0 else 1

    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Page exceeds total pages ({total_pages})"
        )

    skip = (page - 1) * limit

    users = query.offset(skip).limit(limit).all()

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
        "offset": total_pages,   #custom naming
        "data": result
    }


# ======================
# UPDATE USER
# ======================
def update_user(user_id: UUID, data, db: Session):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.email:
        user.email = data.email

    if data.role_ids:
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

    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}