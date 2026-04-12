from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserLogin
from app.services.auth_service import login_user
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.security import create_access_token
from app.core.dependencies import get_current_user

router = APIRouter()


# ======================
# LOGIN
# ======================
@router.post("/auth/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
    response: Response = None
):
    tokens = login_user(data, db)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = tokens

    # ✅ Store ONLY refresh token in cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax", 
        secure=False 
    )

    # ✅ Return access token
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# ======================
# REFRESH TOKEN
# ======================
@router.post("/auth/refresh")
def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = int(payload["sub"])

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # ✅ Create new access token
        new_access_token = create_access_token(
            {"sub": str(user.id)},
            timedelta(minutes=30)
        )

        # ✅ Return access token (NO cookie for access token)
        return {
            "message": "Token refreshed",
            "access_token": new_access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }

    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


# ======================
# CURRENT USER
# ======================
@router.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }