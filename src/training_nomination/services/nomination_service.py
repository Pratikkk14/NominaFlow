"""Nomination workflow business service layer."""

from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from training_nomination.models.audit_event import AuditEvent
from training_nomination.models.nomination import NominationStatus, TrainingNomination
from training_nomination.models.user import User
from training_nomination.schemas.nomination import NominationCreate, NominationUpdate
from training_nomination.services.state_machine import validate_state_transition


def log_audit_event(
    db: Session,
    nomination_id: str,
    user_id: str,
    event_type: str,
    comment: str | None = None,
) -> AuditEvent:
    """Record an immutable audit event for traceability."""
    event = AuditEvent(
        nomination_id=nomination_id,
        user_id=user_id,
        event_type=event_type,
        comment=comment,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(event)
    return event


def create_nomination(
    db: Session,
    user: User,
    data: NominationCreate,
) -> TrainingNomination:
    """Create a new training nomination in DRAFT state."""
    nomination = TrainingNomination(
        employee_id=user.id,
        title=data.title,
        provider=data.provider,
        description=data.description,
        training_type=data.training_type,
        training_date=data.training_date,
        duration=data.duration,
        cost=data.cost,
        justification=data.justification,
        status=NominationStatus.DRAFT.value,
    )
    db.add(nomination)
    db.flush()

    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=user.id,
        event_type="NOMINATION_CREATED",
        comment=f"Nomination '{data.title}' created as DRAFT.",
    )
    db.commit()
    db.refresh(nomination)
    return nomination


def update_nomination_draft(
    db: Session,
    nomination_id: str,
    user: User,
    data: NominationUpdate,
) -> TrainingNomination:
    """Update an existing nomination in DRAFT status."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    # Only author (or admin) can update draft
    if nomination.employee_id != user.id and user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own nominations.",
        )

    if nomination.status != NominationStatus.DRAFT.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot edit nomination in '{nomination.status}' state. Only DRAFT nominations can be updated.",
        )

    update_dict = data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        if value is not None:
            setattr(nomination, field, value)

    nomination.updated_at = datetime.now(timezone.utc)
    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=user.id,
        event_type="DRAFT_UPDATED",
        comment="Draft nomination updated.",
    )
    db.commit()
    db.refresh(nomination)
    return nomination


def submit_nomination(
    db: Session,
    nomination_id: str,
    user: User,
) -> TrainingNomination:
    """Submit a draft nomination into the review pipeline."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    if nomination.employee_id != user.id and user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit your own nominations.",
        )

    # Validate state transition via FSM
    validate_state_transition(nomination.status, NominationStatus.SUBMITTED)

    nomination.status = NominationStatus.SUBMITTED.value
    nomination.submitted_at = datetime.now(timezone.utc)
    nomination.updated_at = datetime.now(timezone.utc)

    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=user.id,
        event_type="NOMINATION_SUBMITTED",
        comment="Nomination submitted for reviewer evaluation.",
    )
    db.commit()
    db.refresh(nomination)
    return nomination


def start_review(
    db: Session,
    nomination_id: str,
    reviewer: User,
) -> TrainingNomination:
    """Reviewer moves nomination from SUBMITTED to UNDER_REVIEW."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    validate_state_transition(nomination.status, NominationStatus.UNDER_REVIEW)

    nomination.status = NominationStatus.UNDER_REVIEW.value
    nomination.updated_at = datetime.now(timezone.utc)

    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=reviewer.id,
        event_type="REVIEW_STARTED",
        comment=f"Review started by {reviewer.name}.",
    )
    db.commit()
    db.refresh(nomination)
    return nomination


def approve_nomination(
    db: Session,
    nomination_id: str,
    reviewer: User,
    comment: str | None = None,
) -> TrainingNomination:
    """Reviewer approves a nomination."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    validate_state_transition(nomination.status, NominationStatus.APPROVED)

    nomination.status = NominationStatus.APPROVED.value
    nomination.updated_at = datetime.now(timezone.utc)

    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=reviewer.id,
        event_type="NOMINATION_APPROVED",
        comment=comment or f"Nomination approved by {reviewer.name}.",
    )
    db.commit()
    db.refresh(nomination)
    return nomination


def reject_nomination(
    db: Session,
    nomination_id: str,
    reviewer: User,
    comment: str,
) -> TrainingNomination:
    """Reviewer rejects a nomination with mandatory feedback comment."""
    if not comment or not comment.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A non-empty rejection comment is mandatory.",
        )

    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    validate_state_transition(nomination.status, NominationStatus.REJECTED)

    nomination.status = NominationStatus.REJECTED.value
    nomination.updated_at = datetime.now(timezone.utc)

    log_audit_event(
        db=db,
        nomination_id=nomination.id,
        user_id=reviewer.id,
        event_type="NOMINATION_REJECTED",
        comment=f"Rejected: {comment.strip()}",
    )
    db.commit()
    db.refresh(nomination)
    return nomination
