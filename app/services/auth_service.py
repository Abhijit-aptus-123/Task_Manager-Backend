from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta

from app.db.models import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

# =========================
# CONFIG (TOKEN EXPIRY)
# =========================
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# =========================
# PUBLIC REGISTER (USER ONLY)
# =========================
def register_user(data: UserCreate, db: Session):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=data.email,
        password=hash_password(data.password),
        role="user"   # 🔒 always user
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================
# ADMIN CREATE USER
# =========================
def admin_create_user(data: UserCreate, db: Session):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role   # ✅ admin decides
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

    # ✅ FIX: pass expiry
    access_token = create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return access_token, refresh_token