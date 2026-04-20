from fastapi import APIRouter, Depends
from app.core.permission import check_permission

router = APIRouter(prefix="/dashboard")


@router.get("/")
def get_dashboard(user=Depends(check_permission("dashboard", "view"))):
    return {
        "message": "Dashboard data visible",
        "user": user.email
    }