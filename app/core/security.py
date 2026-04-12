from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ======================
# PASSWORD
# ======================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# ======================
# ACCESS TOKEN
# ======================
def create_access_token(data: dict, expires_delta: timedelta):

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ======================
# REFRESH TOKEN
# ======================
def create_refresh_token(data: dict, expires_delta: timedelta):

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({
        "exp": expire,
        "type": "refresh"   # optional but good practice
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)