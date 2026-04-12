from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt

from app.db.database import get_db
from app.db.models import User
from app.core.config import SECRET_KEY, ALGORITHM


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    # ✅ Get Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        # ✅ Extract token
        token = auth_header.split(" ")[1]

        # ✅ Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = int(payload.get("sub"))

        # ✅ Get user
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")