"""Authentication and user Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    """User login request payload."""

    email: str
    password: str


class TokenResponse(BaseModel):
    """Authentication token response payload."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str
    role: str


class UserResponse(BaseModel):
    """Public user response payload."""

    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

