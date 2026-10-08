"""API router package exports."""

from training_nomination.api.admin import router as admin_router
from training_nomination.api.auth import router as auth_router
from training_nomination.api.documents import router as documents_router
from training_nomination.api.nominations import router as nominations_router
from training_nomination.api.reviewer import router as reviewer_router

__all__ = [
    "auth_router",
    "nominations_router",
    "documents_router",
    "reviewer_router",
    "admin_router",
]
