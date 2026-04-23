from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task
)
from app.db.database import get_db
from app.core.permission import check_permission
from app.db.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ======================
# CREATE TASK
# ======================
@router.post("/", response_model=TaskResponse)
def create_task_api(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("task", "create"))
):
    return create_task(data, current_user, db)


# ======================
# GET ALL TASKS
# ======================
@router.get("/", response_model=List[TaskResponse])
def get_tasks_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("task", "view"))
):
    return get_tasks(current_user, db)


# ======================
# GET SINGLE TASK
# ======================
@router.get("/{task_id}", response_model=TaskResponse)
def get_task_api(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("task", "view"))
):
    return get_task_by_id(task_id, current_user, db)


# ======================
# UPDATE TASK
# ======================
@router.put("/{task_id}", response_model=TaskResponse)
def update_task_api(
    task_id: UUID,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("task", "update"))
):
    return update_task(task_id, data, current_user, db)


# ======================
# DELETE TASK
# ======================
@router.delete("/{task_id}")
def delete_task_api(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_permission("task", "delete"))
):
    return delete_task(task_id, current_user, db)