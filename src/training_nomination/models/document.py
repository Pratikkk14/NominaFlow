"""Document attachment ORM model."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from training_nomination.db.base import Base


class Document(Base):
    """Documents database table storing file attachment metadata."""

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nomination_id = Column(
        String(36),
        ForeignKey("training_nominations.id"),
        nullable=False,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    nomination = relationship("TrainingNomination", back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document(id='{self.id}', file_name='{self.file_name}')>"
