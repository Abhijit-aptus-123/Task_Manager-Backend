from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import hash_password, verify_password, create_token

def register_user(data, db: Session):
    user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    return user

def login_user(data, db: Session):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        return None

    return create_token({"user_id": user.id, "role": user.role})