from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.database import Base, engine, get_db

from app.schemas.task import TaskCreate, TaskUpdate

from app.services.task_service import (
    create_task,
    get_tasks,
    update_task,
    delete_task
)

from app.core.dependencies import get_current_user

# ✅ ROUTERS
from app.routes import auth
from app.routes import admin

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

# ======================
# DATABASE
# ======================
Base.metadata.create_all(bind=engine)

# ======================
# ROUTERS
# ======================
app.include_router(auth.router)
app.include_router(admin.router)


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