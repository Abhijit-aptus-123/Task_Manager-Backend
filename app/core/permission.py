from fastapi import HTTPException, Depends
from app.core.dependencies import get_current_user


def check_permission(module: str, action: str):

    def permission_checker(current_user=Depends(get_current_user)):

        permissions = current_user.permissions or {}

        #  MODULE CHECK
        if module not in permissions:
            raise HTTPException(
                status_code=403,
                detail=f"No access to module: {module}"
            )

        # ACTION CHECK
        if not permissions[module].get(action, False):
            raise HTTPException(
                status_code=403,
                detail=f"{action.upper()} not allowed on {module}"
            )

        return current_user

    return permission_checker