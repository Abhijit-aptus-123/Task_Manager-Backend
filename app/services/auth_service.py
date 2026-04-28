from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta

from app.db.models import User, Role
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

# 🔥 NEW
from app.services.audit_service import log_action


# =========================
# CREATE USER (STRICT ROLE VALIDATION)
# =========================
def admin_create_user(data: UserCreate, db: Session, current_user):

    # 🔍 Check duplicate email
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_count = db.query(User).count()

    # ======================
    #  FIRST USER → ADMIN
    # ======================
    if user_count == 0:
        role_objs = db.query(Role).filter(Role.name == "admin").all()

        if not role_objs:
            raise HTTPException(
                status_code=500,
                detail="Admin role not found"
            )

    # ======================
    #  ALL OTHER USERS
    # ======================
    else:
        if data.role_ids is None or len(data.role_ids) == 0:
            raise HTTPException(
                status_code=400,
                detail="At least one role must be assigned"
            )

        role_objs = db.query(Role).filter(Role.id.in_(data.role_ids)).all()

        if len(role_objs) != len(data.role_ids):
            raise HTTPException(
                status_code=400,
                detail="Invalid role IDs"
            )

    # ======================
    # CREATE USER
    # ======================
    new_user = User(
        email=data.email,
        password=hash_password(data.password),
        roles=role_objs
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #  AUDIT LOG (creator = current_user; first user fallback)
    actor_id = current_user.id if current_user else new_user.id
    log_action(db, actor_id, "create", "user", new_user.id)

    return new_user


# =========================
# LOGIN
# =========================
def login_user(data: UserLogin, db: Session):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return access_token, refresh_token