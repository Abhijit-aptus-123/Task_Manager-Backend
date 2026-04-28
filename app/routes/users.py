from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import admin_create_user
from app.services.user_service import (
    get_users_paginated,
    update_user,
    delete_user
)
from app.core.permission import check_permission

router = APIRouter(prefix="/users")


# ======================
# CREATE USER
# ======================
@router.post("/")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(check_permission("user", "create"))
):
    # pass current user to service
    new_user = admin_create_user(data, db, user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }


# ======================
# GET USERS (EMAIL + MULTI ROLE FILTER)
# ======================
@router.get("/")
def get_all_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    email: Optional[str] = Query(None),
    role_ids: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(check_permission("user", "view"))
):
    return get_users_paginated(page, limit, db, email, role_ids)


# ======================
# UPDATE USER
# ======================
@router.put("/{user_id}")
def update_user_api(
    user_id,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(check_permission("user", "update"))
):
    return update_user(user_id, data, db)


# ======================
# DELETE USER
# ======================
@router.delete("/{user_id}")
def delete_user_api(
    user_id,
    db: Session = Depends(get_db),
    current_user=Depends(check_permission("user", "delete"))
):
    return delete_user(user_id, current_user, db)


# ======================
# GET ALL USERS (NO PERMISSION CHECK)
# ======================
@router.get("/all")
def get_all_users_unrestricted(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
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