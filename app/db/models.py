from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# ======================
# USER MODEL
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)

    # 🔥 Relationship (one user → many tasks)
    tasks = relationship(
        "Task",
        back_populates="assigned_user",
        cascade="all, delete-orphan"
    )


# ======================
# TASK MODEL
# ======================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # ✅ Status with default
    status = Column(String, default="todo", nullable=False)

    assigned_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )

    # 🔥 Relationship (many tasks → one user)
    assigned_user = relationship(
        "User",
        back_populates="tasks"
    )