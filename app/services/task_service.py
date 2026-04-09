from sqlalchemy.orm import Session
from app.db.models import Task
from fastapi import HTTPException

def create_task(data, user, db: Session):
    if user.role != "admin":
        data.assigned_user_id = user.id

    task = Task(**data.dict())
    db.add(task)
    db.commit()
    return task


def get_tasks(user, db: Session):
    if user.role == "admin":
        return db.query(Task).all()
    return db.query(Task).filter(Task.assigned_user_id == user.id).all()


def update_task(task_id, data, user, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(404)

    if user.role != "admin" and task.assigned_user_id != user.id:
        raise HTTPException(403)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    return task


def delete_task(task_id, user, db: Session):
    task = db.query(Task).filter(Task.id == task_id).first()

    if user.role != "admin":
        raise HTTPException(403)

    db.delete(task)
    db.commit()