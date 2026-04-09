from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import *
from app.db.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tasks")

@router.post("/")
def create(data: TaskCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_task(data, user, db)


@router.get("/")
def read(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_tasks(user, db)


@router.put("/{task_id}")
def update(task_id: int, data: TaskUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return update_task(task_id, data, user, db)


@router.delete("/{task_id}")
def delete(task_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_task(task_id, user, db)