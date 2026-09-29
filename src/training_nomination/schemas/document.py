"""Document Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    """Document metadata response payload."""

    id: str
    nomination_id: str
    file_name: str
    file_type: str
    file_size: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

