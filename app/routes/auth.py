from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session, joinedload
from datetime import timedelta
from jose import jwt, JWTError
from uuid import UUID

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserLogin, UserMeResponse
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

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="none",
        secure=True
    )

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

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        #  UUID VALIDATION
        try:
            user_uuid = UUID(user_id)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid user ID format")

        #  ALWAYS LOAD FRESH DATA
        db.expire_all()

        user = (
            db.query(User)
            .options(joinedload(User.roles))
            .filter(User.id == user_uuid)
            .first()
        )

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        #  NEW ACCESS TOKEN
        new_access_token = create_access_token(
            {"sub": str(user.id)},
            timedelta(minutes=30)
        )

        return {
            "message": "Token refreshed",
            "access_token": new_access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "roles": [
                    {
                        "id": role.id,
                        "name": role.name,
                        "permissions": role.permissions
                    }
                    for role in user.roles
                ]
            }
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    except Exception as e:
        print("REFRESH ERROR:", e)
        raise HTTPException(status_code=401, detail="Refresh failed")


# ======================
# CURRENT USER
# ======================
@router.get("/auth/me", response_model=UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "permissions": role.permissions
            }
            for role in current_user.roles
        ]
    }