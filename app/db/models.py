from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user")

    # 🔥 Back reference (optional but recommended)
    tasks = relationship("Task", back_populates="assigned_user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="todo")
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    # 🔥 Relationship to fetch user email
    assigned_user = relationship("User", back_populates="tasks")