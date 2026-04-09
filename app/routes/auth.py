from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user
from app.db.database import get_db

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(data, db)
    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(data, db)

    if not token:
        raise HTTPException(401, detail="Invalid credentials")

    return {"access_token": token}