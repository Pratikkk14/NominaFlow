"""Reviewer decision and workflow API router."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from training_nomination.api.nominations import build_nomination_response
from training_nomination.core.dependencies import require_roles
from training_nomination.db.session import get_db
from training_nomination.models.nomination import NominationStatus, TrainingNomination
from training_nomination.models.user import User
from training_nomination.schemas.nomination import NominationResponse, RejectionRequest
from training_nomination.services.nomination_service import (
    approve_nomination,
    reject_nomination,
    start_review,
)

router = APIRouter(
    prefix="/api/v1/reviewer",
    tags=["Reviewer Workflow"],
    dependencies=[Depends(require_roles(["REVIEWER", "ADMIN"]))],
)


@router.get("/nominations", response_model=list[NominationResponse])
def get_pending_review_queue(
    db: Session = Depends(get_db),
) -> list[NominationResponse]:
    """Retrieve all nominations awaiting review (SUBMITTED or UNDER_REVIEW)."""
    pending = (
        db.query(TrainingNomination)
        .filter(TrainingNomination.status.in_([NominationStatus.SUBMITTED.value, NominationStatus.UNDER_REVIEW.value]))
        .order_by(TrainingNomination.submitted_at.asc())
        .all()
    )
    return [build_nomination_response(n) for n in pending]


@router.post("/nominations/{nomination_id}/start-review", response_model=NominationResponse)
def reviewer_start_review(
    nomination_id: str,
    current_user: User = Depends(require_roles(["REVIEWER", "ADMIN"])),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Start reviewing a nomination (moves to UNDER_REVIEW)."""
    nomination = start_review(db=db, nomination_id=nomination_id, reviewer=current_user)
    return build_nomination_response(nomination)


@router.post("/nominations/{nomination_id}/approve", response_model=NominationResponse)
def reviewer_approve(
    nomination_id: str,
    current_user: User = Depends(require_roles(["REVIEWER", "ADMIN"])),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Approve a training nomination in UNDER_REVIEW status."""
    nomination = approve_nomination(
        db=db,
        nomination_id=nomination_id,
        reviewer=current_user,
    )
    return build_nomination_response(nomination)


@router.post("/nominations/{nomination_id}/reject", response_model=NominationResponse)
def reviewer_reject(
    nomination_id: str,
    payload: RejectionRequest,
    current_user: User = Depends(require_roles(["REVIEWER", "ADMIN"])),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Reject a training nomination with mandatory reason comment."""
    nomination = reject_nomination(
        db=db,
        nomination_id=nomination_id,
        reviewer=current_user,
        comment=payload.comment,
    )
    return build_nomination_response(nomination)
