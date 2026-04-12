from sqlalchemy.orm import Session, joinedload
from app.db.models import Task
from fastapi import HTTPException


# ======================
# CREATE TASK
# ======================
def create_task(data, user, db: Session):

    # 🔐 If not admin → assign task to self
    if user.role != "admin":
        data.assigned_user_id = user.id

    task = Task(
        title=data.title,
        description=data.description,
        assigned_user_id=data.assigned_user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)   # 🔥 important

    return task


# ======================
# GET TASKS
# ======================
def get_tasks(user, db: Session):

    if user.role == "admin":
        return db.query(Task).options(joinedload(Task.assigned_user)).all()

    return (
        db.query(Task)
        .options(joinedload(Task.assigned_user))
        .filter(Task.assigned_user_id == user.id)
        .all()
    )


# ======================
# UPDATE TASK
# ======================
def update_task(task_id, data, user, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 🔐 RBAC check
    if user.role != "admin" and task.assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ======================
# DELETE TASK
# ======================
def delete_task(task_id, user, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}