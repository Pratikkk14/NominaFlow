"""Administrator monitoring and pipeline audit API router."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from training_nomination.api.nominations import build_nomination_response
from training_nomination.core.dependencies import require_roles
from training_nomination.db.session import get_db
from training_nomination.models.audit_event import AuditEvent
from training_nomination.models.nomination import TrainingNomination
from training_nomination.models.user import User
from training_nomination.schemas.audit_event import AuditEventResponse
from training_nomination.schemas.auth import UserResponse
from training_nomination.schemas.nomination import NominationResponse

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Administrator Monitoring"],
    dependencies=[Depends(require_roles(["ADMIN"]))],
)


@router.get("/nominations", response_model=list[NominationResponse])
def get_all_nominations(
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[NominationResponse]:
    """Retrieve all nominations across the organization with optional status filtering."""
    query = db.query(TrainingNomination)
    if status_filter:
        query = query.filter(TrainingNomination.status == status_filter.upper())
    nominations = query.order_by(TrainingNomination.created_at.desc()).all()
    return [build_nomination_response(n) for n in nominations]


@router.get("/audit-events", response_model=list[AuditEventResponse])
def get_all_audit_events(
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
) -> list[AuditEventResponse]:
    """Query global immutable audit event logs."""
    events = db.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(limit).all()
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
        for evt in events
    ]


@router.get("/users", response_model=list[UserResponse])
def list_system_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    """List all registered system users and assigned roles."""
    users = db.query(User).order_by(User.created_at.asc()).all()
    return [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            role=u.role.name if u.role else "EMPLOYEE",
            created_at=u.created_at,
        )
        for u in users
    ]
