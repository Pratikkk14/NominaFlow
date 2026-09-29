"""Training nomination Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from training_nomination.schemas.document import DocumentResponse
from training_nomination.schemas.audit_event import AuditEventResponse


class NominationBase(BaseModel):
    """Common attributes for training nominations."""

    title: str = Field(..., min_length=3, max_length=255, description="Training program title")
    provider: str = Field(..., min_length=2, max_length=255, description="Training provider / vendor")
    description: str = Field(default="", description="Course overview / syllabus details")
    training_type: str = Field(default="Technical", max_length=50, description="Training category")
    training_date: str = Field(..., description="Proposed date of training (YYYY-MM-DD)")
    duration: str = Field(default="1 day", max_length=50, description="Duration (e.g., 3 days, 20 hours)")
    cost: float = Field(default=0.0, ge=0.0, description="Estimated training cost in currency units")
    justification: str = Field(default="", description="Business rationale and justification")


class NominationCreate(NominationBase):
    """Payload to create a new draft training nomination."""

    pass


class NominationUpdate(BaseModel):
    """Payload to update an existing draft training nomination."""

    title: str | None = Field(default=None, min_length=3, max_length=255)
    provider: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    training_type: str | None = None
    training_date: str | None = None
    duration: str | None = None
    cost: float | None = Field(default=None, ge=0.0)
    justification: str | None = None


class RejectionRequest(BaseModel):
    """Payload for rejecting a nomination with a mandatory explanation."""

    comment: str = Field(..., min_length=3, description="Mandatory reason for rejection")


class NominationResponse(NominationBase):
    """Full nomination response payload."""

    id: str
    employee_id: str
    employee_name: str | None = None
    status: str
    created_at: datetime
    submitted_at: datetime | None = None
    updated_at: datetime
    documents: list[DocumentResponse] = []
    audit_events: list[AuditEventResponse] = []

    model_config = ConfigDict(from_attributes=True)

