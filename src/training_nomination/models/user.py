"""User ORM model."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from training_nomination.db.base import Base


class User(Base):
    """Users database table."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    role = relationship("Role", back_populates="users")
    nominations = relationship(
        "TrainingNomination",
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    audit_events = relationship("AuditEvent", back_populates="actor")

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', email='{self.email}')>"
