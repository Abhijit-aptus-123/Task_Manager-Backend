from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate
from app.services.auth_service import admin_create_user
from app.core.dependencies import get_current_user

router = APIRouter()


# ======================
# CREATE USER (ADMIN)
# ======================
@router.post("/admin/users")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    user = admin_create_user(data, db)

    return {
        "message": "User created",
        "user_id": user.id
    }


# ======================
# GET ALL USERS (ADMIN)
# ======================
@router.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ]


# ======================
# UPDATE USER ROLE (ADMIN)
# ======================
@router.put("/admin/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ✅ Only admin allowed
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin allowed")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ❌ Admin cannot change their own role
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot change their own role"
        )

    # ❌ Validate role
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    # ✅ Update role
    user.role = role

    db.commit()
    db.refresh(user)

    return {
        "message": "User role updated",
        "user_id": user.id,
        "new_role": user.role
    }