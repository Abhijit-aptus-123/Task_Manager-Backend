from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt

# DB
from app.db.database import Base, engine, get_db
from app.db.models import User  # ✅ IMPORTANT

# Schemas
from app.schemas.user import UserCreate, UserLogin
from app.schemas.task import TaskCreate, TaskUpdate

# Services
from app.services.auth_service import (
    login_user,
    admin_create_user
)
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task
)

# Auth
from app.core.dependencies import get_current_user
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.security import create_access_token

app = FastAPI()

# ======================
# ✅ CORS CONFIG
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://mainstream-magnetic-leader-jets.trycloudflare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# ======================
# AUTH - LOGIN
# ======================
@app.post("/auth/login")
def login(data: UserLogin,
          response: Response,
          db: Session = Depends(get_db)):

    tokens = login_user(data, db)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = tokens

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite="none",
        secure=True
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="none",
        secure=True
    )

    return {"message": "Login successful"}


# ======================
# AUTH - REFRESH TOKEN
# ======================
@app.post("/auth/refresh")
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

        # ✅ Fetch user
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # ✅ Create new access token
        new_access_token = create_access_token(
            {"sub": str(user.id)},
            timedelta(minutes=30)
        )

        # ✅ Set cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=1800,
            samesite="none",
            secure=True
        )

        # ✅ Return token + user info
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
# AUTH - GET CURRENT USER
# ======================
@app.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


# ======================
# ADMIN - CREATE USER
# ======================
@app.post("/admin/users")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    user = admin_create_user(data, db)

    return {
        "message": "User created",
        "user_id": user.id
    }


# ======================
# ADMIN - GET ALL USERS
# ======================
@app.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]


# ======================
# TASK ENDPOINTS
# ======================
@app.post("/tasks")
def create(
    data: TaskCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_task(data, user, db)


@app.get("/tasks")
def read(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_tasks(user, db)


@app.put("/tasks/{task_id}")
def update(
    task_id: int,
    data: TaskUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return update_task(task_id, data, user, db)


@app.delete("/tasks/{task_id}")
def delete(
    task_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return delete_task(task_id, user, db)