"""Finite State Machine (FSM) for training nomination lifecycle."""

from fastapi import HTTPException, status
from training_nomination.models.nomination import NominationStatus

# Allowed transitions mapping: source_state -> set of target_states
VALID_TRANSITIONS: dict[NominationStatus, set[NominationStatus]] = {
    NominationStatus.DRAFT: {NominationStatus.SUBMITTED},
    NominationStatus.SUBMITTED: {NominationStatus.UNDER_REVIEW},
    NominationStatus.UNDER_REVIEW: {NominationStatus.APPROVED, NominationStatus.REJECTED},
    NominationStatus.APPROVED: set(),  # Terminal state
    NominationStatus.REJECTED: set(),  # Terminal state
}


def validate_state_transition(
    current_status: str | NominationStatus,
    target_status: str | NominationStatus,
) -> None:
    """Validate whether transitioning from current_status to target_status is permitted.

    Raises HTTPException(400) if transition is invalid.
    """
    try:
        source_enum = (
            current_status
            if isinstance(current_status, NominationStatus)
            else NominationStatus(current_status)
        )
        target_enum = (
            target_status
            if isinstance(target_status, NominationStatus)
            else NominationStatus(target_status)
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid workflow state provided: {err}",
        ) from err

    allowed_targets = VALID_TRANSITIONS.get(source_enum, set())
    if target_enum not in allowed_targets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid workflow state transition: Cannot transition nomination from "
                f"'{source_enum.value}' to '{target_enum.value}'. "
                f"Allowed transitions from '{source_enum.value}': "
                f"{[s.value for s in allowed_targets] or 'None (Terminal State)'}."
            ),
        )
