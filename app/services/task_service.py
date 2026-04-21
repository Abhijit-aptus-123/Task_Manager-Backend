from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.db.models import Task, User


# ======================
# HELPER: ADMIN CHECK 
# ======================
def is_admin(user: User):
    # multi-role support
    if not user.roles:
        return False
    return any(role.name.lower() == "admin" for role in user.roles)


# ======================
# HELPER: CLEAN USER ID
# ======================
def get_valid_user_id(input_id, current_user_id):
    if input_id in [None, "", 0]:
        return current_user_id
    return input_id


# ======================
# CREATE TASK
# ======================
def create_task(data, user: User, db: Session):

    assigned_user_id = get_valid_user_id(data.assigned_user_id, user.id)

    assigned_user = db.query(User).filter(User.id == assigned_user_id).first()
    if not assigned_user:
        raise HTTPException(status_code=404, detail="Assigned user not found")

    task = Task(
        title=data.title,
        description=data.description,
        assigned_user_id=assigned_user_id,
        status=data.status or "todo"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# ======================
# GET TASKS
# ======================
def get_tasks(user: User, db: Session):

    query = db.query(Task).options(joinedload(Task.assigned_user))

    #  Admin → all tasks
    if is_admin(user):
        return query.all()

    # Normal user → only own tasks
    return query.filter(Task.assigned_user_id == user.id).all()


# ======================
# GET SINGLE TASK
# ======================
def get_task_by_id(task_id: int, user: User, db: Session):

    task = (
        db.query(Task)
        .options(joinedload(Task.assigned_user))
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Access control
    if not is_admin(user) and task.assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return task


# ======================
# UPDATE TASK
# ======================
def update_task(task_id: int, data, user: User, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only owner or admin
    if not is_admin(user) and task.assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_data = data.dict(exclude_unset=True, by_alias=False)

    # Handle reassignment
    if "assigned_user_id" in update_data:
        new_user_id = get_valid_user_id(update_data["assigned_user_id"], user.id)

        assigned_user = db.query(User).filter(User.id == new_user_id).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

        update_data["assigned_user_id"] = new_user_id

    # Apply updates
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ======================
# DELETE TASK
# ======================
def delete_task(task_id: int, user: User, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # RBAC handled at route level (check_permission)
    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}