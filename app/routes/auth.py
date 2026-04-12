from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user, refresh_access_token

router = APIRouter()


# ======================
# PUBLIC REGISTER
# ======================
@router.post("/auth/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(data, db)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


# ======================
# LOGIN
# ======================
@router.post("/auth/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
    response: Response = None   # ⚠️ FastAPI injects it automatically
):
    tokens = login_user(data, db)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = tokens

    # 🍪 Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax"
    )

    return {"message": "Login successful"}


# ======================
# REFRESH TOKEN
# ======================
@router.post("/auth/refresh")
def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    new_access_token = refresh_access_token(refresh_token)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        samesite="lax"
    )

    return {"message": "Access token refreshed"}