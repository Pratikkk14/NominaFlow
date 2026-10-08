"""Role ORM model and role type enumeration."""

import enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from training_nomination.db.base import Base


class RoleType(str, enum.Enum):
    """Supported user role types."""

    EMPLOYEE = "EMPLOYEE"
    REVIEWER = "REVIEWER"
    ADMIN = "ADMIN"


class Role(Base):
    """Roles database table."""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}')>"
