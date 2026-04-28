from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.db.database import get_db
from app.db.models import Task, User
from app.core.permission import check_permission

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/tasks")
def task_analytics(
    db: Session = Depends(get_db),

    #  analytics permission required
    current_user: User = Depends(check_permission("analytics", "view"))
):
    # ======================
    # PERMISSIONS
    # ======================
    analytics_perms = current_user.permissions.get("analytics", {})

    # ======================
    # BASE QUERY
    # ======================
    query = db.query(
        func.count(Task.id).label("total"),

        func.sum(
            case((Task.status == "done", 1), else_=0)
        ).label("completed"),

        func.sum(
            case((Task.status == "todo", 1), else_=0)
        ).label("pending")
    )

    # ======================
    # RBAC LOGIC  FINAL
    # ======================
    if not analytics_perms.get("view_all"):
        #  Only own analytics
        query = query.filter(Task.assigned_user_id == current_user.id)

    # ======================
    # RESULT
    # ======================
    result = query.first()

    return {
        "total_tasks": result.total or 0,
        "completed_tasks": result.completed or 0,
        "pending_tasks": result.pending or 0
    }