from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from uuid import UUID

from app.db.models import Task, User
from app.services.audit_service import log_action
from app.services.notification_service import create_notification


# ======================
# HELPERS
# ======================
def get_task_permissions(user: User):
    return user.permissions.get("task", {})


def get_task_scope(user: User):
    return user.permissions.get("task_scope", {})


def get_valid_user_id(input_id, current_user_id):
    if input_id in [None, "", 0]:
        return current_user_id
    return input_id


# ======================
# CREATE TASK
# ======================
def create_task(data, user: User, db: Session):

    perms = get_task_permissions(user)
    scope = get_task_scope(user)

    if not (perms.get("create") or scope.get("create_all")):
        raise HTTPException(status_code=403, detail="No create permission")

    assigned_user_id = get_valid_user_id(data.assigned_user_id, user.id)

    if not scope.get("create_all") and assigned_user_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot assign tasks to others")

    assigned_user = db.query(User).filter(User.id == assigned_user_id).first()
    if not assigned_user:
        raise HTTPException(status_code=404, detail="Assigned user not found")

    task = Task(
        title=data.title,
        description=data.description,
        assigned_user_id=assigned_user_id,
        created_by=user.id,
        status=data.status or "todo"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    # AUDIT
    log_action(db, user.id, "create", "task", task.id)

    #  Notify assignee
    if assigned_user_id != user.id:
        create_notification(
            db,
            assigned_user_id,
            f"You have been assigned a new task by {user.email}"
        )

    return task


# ======================
# GET TASKS
# ======================
def get_tasks(user: User, db: Session, title: str = None, description: str = None):

    perms = get_task_permissions(user)
    scope = get_task_scope(user)

    query = db.query(Task).options(joinedload(Task.assigned_user))

    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))

    if description:
        query = query.filter(Task.description.ilike(f"%{description}%"))

    if scope.get("view_all"):
        return query.all()

    if perms.get("view"):
        return query.filter(Task.assigned_user_id == user.id).all()

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
    scope = get_task_scope(user)

    if scope.get("view_all"):
        return task

    if perms.get("view") and task.assigned_user_id == user.id:
        return task

    raise HTTPException(status_code=403, detail="Not allowed")


# ======================
# UPDATE TASK
# ======================
def update_task(task_id: UUID, data, user: User, db: Session):

    #  Load assigner relation
    task = (
        db.query(Task)
        .options(joinedload(Task.created_user))
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perms = get_task_permissions(user)
    scope = get_task_scope(user)

    if scope.get("update_all"):
        pass
    elif perms.get("update") and task.assigned_user_id == user.id:
        pass
    else:
        raise HTTPException(status_code=403, detail="No update permission")

    # Track old status
    old_status = task.status

    update_data = data.dict(exclude_unset=True)

    # ======================
    # HANDLE REASSIGNMENT
    # ======================
    if "assigned_user_id" in update_data:
        new_user_id = get_valid_user_id(update_data["assigned_user_id"], user.id)

        if not scope.get("update_all") and new_user_id != user.id:
            raise HTTPException(status_code=403, detail="Cannot reassign task")

        assigned_user = db.query(User).filter(User.id == new_user_id).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

        update_data["assigned_user_id"] = new_user_id

    # ======================
    # APPLY UPDATE
    # ======================
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    # AUDIT
    log_action(db, user.id, "update", "task", task.id)

    # ======================
    # NOTIFICATION LOGIC (FINAL)
    # ======================

    assigner_email = task.created_user.email if task.created_user else "Unknown"

    # No self notification
    if task.created_by and task.created_by != user.id:

        #  Status changed
        if "status" in update_data and old_status != task.status:

            if task.status == "in_progress":
                create_notification(
                    db,
                    task.created_by,
                    f"{user.email} updated your task (assigned by {assigner_email}) → Work is in progress"
                )

            elif task.status == "done":
                create_notification(
                    db,
                    task.created_by,
                    f"{user.email} completed your task (assigned by {assigner_email})"
                )

        else:
            #  Generic update
            create_notification(
                db,
                task.created_by,
                f"{user.email} updated your task (assigned by {assigner_email})"
            )

    return task


# ======================
# DELETE TASK
# ======================
def delete_task(task_id: UUID, user: User, db: Session):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perms = get_task_permissions(user)
    scope = get_task_scope(user)

    if scope.get("delete_all"):
        pass
    elif perms.get("delete") and task.assigned_user_id == user.id:
        pass
    else:
        raise HTTPException(status_code=403, detail="No delete permission")

    db.delete(task)
    db.commit()

    # AUDIT
    log_action(db, user.id, "delete", "task", task_id)

    return {"message": "Task deleted successfully"}