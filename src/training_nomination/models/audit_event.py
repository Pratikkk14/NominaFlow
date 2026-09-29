"""Audit event log ORM model."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from training_nomination.db.base import Base


class AuditEvent(Base):
    """Audit events database table recording immutable state transitions."""

    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nomination_id = Column(
        String(36),
        ForeignKey("training_nominations.id"),
        nullable=False,
        index=True,
    )
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    nomination = relationship("TrainingNomination", back_populates="audit_events")
    actor = relationship("User", back_populates="audit_events")

    def __repr__(self) -> str:
        return f"<AuditEvent(id='{self.id}', event_type='{self.event_type}', timestamp='{self.timestamp}')>"
