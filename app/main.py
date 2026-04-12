from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db
from app.db.models import User

from app.schemas.user import UserCreate
from app.schemas.task import TaskCreate, TaskUpdate

from app.services.auth_service import admin_create_user
from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task
)

from app.core.dependencies import get_current_user

# ✅ Import auth router
from app.routes import auth

app = FastAPI()

# ======================
# CORS CONFIG
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mainstream-magnetic-leader-jets.trycloudflare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# ✅ Include auth routes
app.include_router(auth.router)


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