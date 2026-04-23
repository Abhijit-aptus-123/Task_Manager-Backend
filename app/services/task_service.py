from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from uuid import UUID

from app.db.models import Task, User


# ======================
# HELPER: GET TASK PERMISSIONS
# ======================
def get_task_permissions(user: User):
    return user.permissions.get("task", {})


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
# GET TASKS (PERMISSION BASED)
# ======================
def get_tasks(user: User, db: Session):

    perms = get_task_permissions(user)

    query = db.query(Task).options(joinedload(Task.assigned_user))

    #  VIEW ALL TASKS
    if perms.get("view_all"):
        return query.all()

    #  VIEW OWN TASKS
    if perms.get("view"):
        return query.filter(Task.assigned_user_id == user.id).all()

    #  NO ACCESS
    raise HTTPException(status_code=403, detail="No permission to view tasks")


# ======================
# GET SINGLE TASK
# ======================
def get_task_by_id(task_id: UUID, user: User, db: Session):

    task = (
        db.query(Task)
        .options(joinedload(Task.assigned_user))
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perms = get_task_permissions(user)

    #  FULL ACCESS
    if perms.get("view_all"):
        return task

    # OWN TASK ACCESS
    if perms.get("view") and task.assigned_user_id == user.id:
        return task

    raise HTTPException(status_code=403, detail="Not allowed")


# ======================
# UPDATE TASK
# ======================
def update_task(task_id: UUID, data, user: User, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perms = get_task_permissions(user)

    #  NO UPDATE PERMISSION
    if not perms.get("update"):
        raise HTTPException(status_code=403, detail="No update permission")

    #  NOT OWNER (if not view_all)
    if not perms.get("view_all") and task.assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_data = data.dict(exclude_unset=True, by_alias=False)

    #  HANDLE REASSIGNMENT
    if "assigned_user_id" in update_data:
        new_user_id = get_valid_user_id(update_data["assigned_user_id"], user.id)

        assigned_user = db.query(User).filter(User.id == new_user_id).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

        update_data["assigned_user_id"] = new_user_id

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# ======================
# DELETE TASK
# ======================
def delete_task(task_id: UUID, user: User, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perms = get_task_permissions(user)

    # NO DELETE PERMISSION
    if not perms.get("delete"):
        raise HTTPException(status_code=403, detail="No delete permission")

    #  NOT OWNER (if not view_all)
    if not perms.get("view_all") and task.assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}