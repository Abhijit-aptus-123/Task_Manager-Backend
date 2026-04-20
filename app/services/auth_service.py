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


# =========================
# CREATE USER (MULTI-ROLE)
# =========================
def admin_create_user(data: UserCreate, db: Session):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    #  First user = admin
    user_count = db.query(User).count()
    role_names = ["admin"] if user_count == 0 else data.roles

    #  Fetch roles
    role_objs = db.query(Role).filter(Role.name.in_(role_names)).all()

    if len(role_objs) != len(role_names):
        raise HTTPException(status_code=400, detail="Invalid role(s)")

    new_user = User(
        email=data.email,
        password=hash_password(data.password),
        roles=role_objs   # ✅ FIX
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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