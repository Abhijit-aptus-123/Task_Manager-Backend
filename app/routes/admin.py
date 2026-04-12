from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import admin_create_user
from app.core.dependencies import get_current_user

router = APIRouter()


# ======================
# ADMIN CREATE USER
# ======================
@router.post("/admin/users")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    user = admin_create_user(data, db)

    return {
        "message": "User created by admin",
        "user_id": user.id
    }