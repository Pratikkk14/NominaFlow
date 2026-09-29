"""Training nomination ORM model and status enumeration."""

import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from training_nomination.db.base import Base


class NominationStatus(str, enum.Enum):
    """Training nomination lifecycle statuses."""

    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class TrainingNomination(Base):
    """Training nominations database table."""

    __tablename__ = "training_nominations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    employee_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    provider = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, default="")
    training_type = Column(String(50), nullable=False, default="Technical")
    training_date = Column(String(50), nullable=False)
    duration = Column(String(50), nullable=False, default="1 day")
    cost = Column(Float, nullable=False, default=0.0)
    justification = Column(Text, nullable=False, default="")
    status = Column(
        String(30),
        nullable=False,
        default=NominationStatus.DRAFT.value,
        index=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    employee = relationship("User", back_populates="nominations")
    documents = relationship(
        "Document",
        back_populates="nomination",
        cascade="all, delete-orphan",
    )
    audit_events = relationship(
        "AuditEvent",
        back_populates="nomination",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<TrainingNomination(id='{self.id}', title='{self.title}', status='{self.status}')>"
