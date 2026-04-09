from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# DB
from app.db.database import Base, engine, get_db

# Schemas
from app.schemas.user import UserCreate, UserLogin
from app.schemas.task import TaskCreate, TaskUpdate

# Services
from app.services.auth_service import register_user, login_user
from app.services.task_service import create_task, get_tasks, update_task, delete_task

# Auth
from app.core.dependencies import get_current_user

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# ======================
# AUTH ENDPOINTS
# ======================

@app.post("/auth/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(data, db)
    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


@app.post("/auth/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(data, db)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ======================
# TASK ENDPOINTS
# ======================

@app.post("/tasks")
def create(data: TaskCreate,
           user=Depends(get_current_user),
           db: Session = Depends(get_db)):
    return create_task(data, user, db)


@app.get("/tasks")
def read(user=Depends(get_current_user),
         db: Session = Depends(get_db)):
    return get_tasks(user, db)


@app.put("/tasks/{task_id}")
def update(task_id: int,
           data: TaskUpdate,
           user=Depends(get_current_user),
           db: Session = Depends(get_db)):
    return update_task(task_id, data, user, db)


@app.delete("/tasks/{task_id}")
def delete(task_id: int,
           user=Depends(get_current_user),
           db: Session = Depends(get_db)):
    return delete_task(task_id, user, db)