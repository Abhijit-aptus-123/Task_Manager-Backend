from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import get_db
from app.services.notification_service import (
    get_user_notifications,
    mark_as_read
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# GET MY NOTIFICATIONS
@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_notifications(db, current_user.id)


# MARK AS READ
@router.put("/{notification_id}")
def read_notification(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return mark_as_read(db, notification_id, current_user.id)