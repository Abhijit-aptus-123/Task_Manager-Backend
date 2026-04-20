from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import *
from app.db.database import get_db
from app.core.permission import check_permission

router = APIRouter(prefix="/tasks")


# ======================
# CREATE TASK
# ======================
@router.post("/", response_model=TaskResponse)
def create(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user = Depends(check_permission("task", "create"))
):
    return create_task(data, user, db)


# ======================
# GET TASKS
# ======================
@router.get("/", response_model=List[TaskResponse])
def read(
    db: Session = Depends(get_db),
    user = Depends(check_permission("task", "view"))
):
    return get_tasks(user, db)


# ======================
# GET SINGLE TASK
# ======================
@router.get("/{task_id}", response_model=TaskResponse)
def get_one(
    task_id: int,
    db: Session = Depends(get_db),
    user = Depends(check_permission("task", "view"))
):
    return get_task_by_id(task_id, user, db)


# ======================
# UPDATE TASK
# ======================
@router.put("/{task_id}", response_model=TaskResponse)
def update(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    user = Depends(check_permission("task", "update"))
):
    return update_task(task_id, data, user, db)


# ======================
# DELETE TASK
# ======================
@router.delete("/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    user = Depends(check_permission("task", "delete"))
):
    return delete_task(task_id, user, db)