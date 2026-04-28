from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from math import ceil
from typing import Optional
from app.core.permission import check_permission
from app.db.database import get_db
from app.db.models import AuditLog, User

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/logs")
def get_logs(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, le=100, description="Items per page"),
    email: Optional[str] = Query(None, description="Filter by user email"),

    db: Session = Depends(get_db),
    user=Depends(check_permission("audit", "view"))
):
    # ======================
    # BASE QUERY
    # ======================
    query = (
        db.query(AuditLog)
        .options(joinedload(AuditLog.user))
        .join(User, AuditLog.user_id == User.id)
    )

    # ======================
    # FILTER BY EMAIL
    # ======================
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    # ======================
    # TOTAL COUNT
    # ======================
    total = query.count()

    total_pages = ceil(total / limit) if total > 0 else 1

    if page > total_pages:
        raise HTTPException(
            status_code=400,
            detail=f"Page exceeds total pages ({total_pages})"
        )

    # ======================
    # PAGINATION
    # ======================
    skip = (page - 1) * limit

    logs = (
        query
        .order_by(AuditLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # ======================
    # RESPONSE
    # ======================
    data = [
        {
            "id": log.id,
            "email": log.user.email if log.user else None,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "timestamp": log.timestamp
        }
        for log in logs
    ]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "offset": total_pages,   # FIXED (instead of offset)
        "data": data
    }