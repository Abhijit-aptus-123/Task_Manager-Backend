from pydantic import BaseModel, EmailStr

# ======================
# CREATE USER (Register)
# ======================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


# ======================
# LOGIN USER
# ======================
class UserLogin(BaseModel):
    email: EmailStr
    password: str