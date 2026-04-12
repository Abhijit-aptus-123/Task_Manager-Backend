from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import jwt

from app.db.database import get_db
from app.db.models import User
from app.core.config import SECRET_KEY, ALGORITHM


def get_current_user(request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")