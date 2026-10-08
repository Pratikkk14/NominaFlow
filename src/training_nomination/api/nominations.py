"""Training nominations API router."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from training_nomination.core.dependencies import get_current_user
from training_nomination.db.session import get_db
from training_nomination.models.nomination import TrainingNomination
from training_nomination.models.user import User
from training_nomination.schemas.audit_event import AuditEventResponse
from training_nomination.schemas.document import DocumentResponse
from training_nomination.schemas.nomination import (
    NominationCreate,
    NominationResponse,
    NominationUpdate,
)
from training_nomination.services.nomination_service import (
    create_nomination,
    submit_nomination,
    update_nomination_draft,
)

router = APIRouter(prefix="/api/v1/nominations", tags=["Nominations"])


def build_nomination_response(nomination: TrainingNomination) -> NominationResponse:
    """Helper formatting nomination ORM instance into response schema."""
    return NominationResponse(
        id=nomination.id,
        employee_id=nomination.employee_id,
        employee_name=nomination.employee.name if nomination.employee else "Unknown",
        title=nomination.title,
        provider=nomination.provider,
        description=nomination.description,
        training_type=nomination.training_type,
        training_date=nomination.training_date,
        duration=nomination.duration,
        cost=nomination.cost,
        justification=nomination.justification,
        status=nomination.status,
        created_at=nomination.created_at,
        submitted_at=nomination.submitted_at,
        updated_at=nomination.updated_at,
        documents=[DocumentResponse.model_validate(doc) for doc in nomination.documents],
        audit_events=[
            AuditEventResponse(
                id=evt.id,
                nomination_id=evt.nomination_id,
                user_id=evt.user_id,
                actor_name=evt.actor.name if evt.actor else "System",
                event_type=evt.event_type,
                comment=evt.comment,
                timestamp=evt.timestamp,
            )
            for evt in nomination.audit_events
        ],
    )


@router.post("", response_model=NominationResponse, status_code=status.HTTP_201_CREATED)
def create_new_nomination(
    payload: NominationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Create a new training nomination in DRAFT status."""
    nomination = create_nomination(db=db, user=current_user, data=payload)
    return build_nomination_response(nomination)


@router.get("", response_model=list[NominationResponse])
def list_my_nominations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[NominationResponse]:
    """Retrieve all nominations submitted or drafted by the current user."""
    nominations = (
        db.query(TrainingNomination)
        .filter(TrainingNomination.employee_id == current_user.id)
        .order_by(TrainingNomination.created_at.desc())
        .all()
    )
    return [build_nomination_response(n) for n in nominations]


@router.get("/{nomination_id}", response_model=NominationResponse)
def get_nomination_details(
    nomination_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Get complete nomination details by ID."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    # Authorization check
    user_role = current_user.role.name if current_user.role else "EMPLOYEE"
    if nomination.employee_id != current_user.id and user_role not in ["REVIEWER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You cannot view nominations created by another user.",
        )

    return build_nomination_response(nomination)


@router.put("/{nomination_id}", response_model=NominationResponse)
def update_draft_nomination(
    nomination_id: str,
    payload: NominationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Update an existing nomination in DRAFT status."""
    nomination = update_nomination_draft(
        db=db,
        nomination_id=nomination_id,
        user=current_user,
        data=payload,
    )
    return build_nomination_response(nomination)


@router.post("/{nomination_id}/submit", response_model=NominationResponse)
def submit_draft_nomination(
    nomination_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NominationResponse:
    """Submit a draft nomination into the review queue."""
    nomination = submit_nomination(
        db=db,
        nomination_id=nomination_id,
        user=current_user,
    )
    return build_nomination_response(nomination)


@router.get("/{nomination_id}/status")
def get_nomination_status(
    nomination_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Get the live status and lifecycle progress of a nomination."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    return {
        "id": nomination.id,
        "title": nomination.title,
        "status": nomination.status,
        "submitted_at": nomination.submitted_at,
        "updated_at": nomination.updated_at,
    }


@router.get("/{nomination_id}/history", response_model=list[AuditEventResponse])
def get_nomination_history(
    nomination_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AuditEventResponse]:
    """Retrieve full audit event log for a nomination."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    return [
        AuditEventResponse(
            id=evt.id,
            nomination_id=evt.nomination_id,
            user_id=evt.user_id,
            actor_name=evt.actor.name if evt.actor else "System",
            event_type=evt.event_type,
            comment=evt.comment,
            timestamp=evt.timestamp,
        )
        for evt in nomination.audit_events
    ]
