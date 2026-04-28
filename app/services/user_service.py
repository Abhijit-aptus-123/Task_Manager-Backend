from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from uuid import UUID
from typing import Optional
from math import ceil

from app.db.models import User, Role
from app.services.audit_service import log_action   # NEW


# ======================
# GET USERS (UNCHANGED)
# ======================
def get_users_paginated(page: int, limit: int, db: Session, email: Optional[str] = None, role_ids: Optional[str] = None):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination values")

    query = db.query(User)

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    if role_ids:
        role_list = [r.strip() for r in role_ids.split(",") if r.strip()]

        query = (
            query.join(User.roles)
            .filter(Role.id.in_(role_list))
            .group_by(User.id)
            .having(func.count(Role.id) == len(role_list))
        )

    total = query.count()
    total_pages = ceil(total / limit) if total > 0 else 1

    if page > total_pages:
        raise HTTPException(status_code=400, detail=f"Page exceeds total pages ({total_pages})")

    skip = (page - 1) * limit
    users = query.offset(skip).limit(limit).all()

    result = [
        {
            "id": user.id,
            "email": user.email,
            "roles": [{"id": role.id, "name": role.name} for role in user.roles],
            "status": "Active"
        }
        for user in users
    ]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": total_pages,
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

    # AUDIT LOG
    log_action(db, user.id, "update", "user", user.id)

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
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    db.delete(user)
    db.commit()

    # AUDIT LOG
    log_action(db, current_user.id, "delete", "user", user_id)

    return {"message": "User deleted successfully"}