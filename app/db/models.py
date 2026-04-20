import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


# ======================
#  ASSOCIATION TABLE (UUID FIXED)
# ======================
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)


# ======================
# ROLE MODEL
# ======================
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    permissions = Column(JSON, default=dict)

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )


# ======================
# USER MODEL (UUID)
# ======================
class User(Base):
    __tablename__ = "users"

    #  UUID PRIMARY KEY
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    #  MANY-TO-MANY ROLES
    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users"
    )

    #  MERGED PERMISSIONS
    @property
    def permissions(self):
        final_permissions = {}

        for role in self.roles:
            if not role.permissions:
                continue

            for module, actions in role.permissions.items():
                if module not in final_permissions:
                    final_permissions[module] = {
                        "view": False,
                        "create": False,
                        "update": False,
                        "delete": False
                    }

                for action, value in actions.items():
                    final_permissions[module][action] = (
                        final_permissions[module][action] or value
                    )

        return final_permissions


# ======================
# TASK MODEL (UUID FK)
# ======================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo", nullable=False)

    #  UUID FOREIGN KEY
    assigned_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )

    assigned_user = relationship("User")