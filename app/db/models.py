from sqlalchemy import Column, String, ForeignKey, JSON, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .database import Base


# ======================
# ASSOCIATION TABLE
# ======================
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE")),
)


# ======================
# ROLE MODEL
# ======================
class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    permissions = Column(JSON, default=dict)

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )


# ======================
# USER MODEL
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

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
# TASK MODEL
# ======================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo", nullable=False)

    assigned_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )

    assigned_user = relationship("User")