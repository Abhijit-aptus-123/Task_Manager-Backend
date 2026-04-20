from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from app.db.models import User, Role


# ======================
# GET USERS (PAGINATION)
# ======================
def get_users_paginated(page: int, limit: int, db: Session):

    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination values")

    skip = (page - 1) * limit
    total = db.query(User).count()

    users = db.query(User).offset(skip).limit(limit).all()

    result = [
        {
            "id": user.id,
            "email": user.email,
            "roles": user.roles,   # ✅ FIX
            "status": "Active"
        }
        for user in users
    ]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": result
    }


# ======================
# UPDATE USER (MULTI-ROLE)
# ======================
def update_user(user_id: UUID, data, db: Session):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.email:
        user.email = data.email

    if data.roles:
        role_objs = db.query(Role).filter(Role.name.in_(data.roles)).all()

        if len(role_objs) != len(data.roles):
            raise HTTPException(status_code=400, detail="Invalid role(s)")

        user.roles = role_objs   # ✅ FIX

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

    #  Prevent self delete
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}