"""Audit event Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditEventResponse(BaseModel):
    """Audit event log response payload."""

    id: str
    nomination_id: str
    user_id: str
    actor_name: str | None = None
    event_type: str
    comment: str | None = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

