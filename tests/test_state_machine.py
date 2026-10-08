"""Finite State Machine unit tests."""

import pytest
from fastapi import HTTPException

from training_nomination.models.nomination import NominationStatus
from training_nomination.services.state_machine import validate_state_transition


def test_valid_transitions():
    """Verify that all legal state machine transitions pass without exception."""
    # DRAFT -> SUBMITTED
    validate_state_transition(NominationStatus.DRAFT, NominationStatus.SUBMITTED)

    # SUBMITTED -> UNDER_REVIEW
    validate_state_transition(NominationStatus.SUBMITTED, NominationStatus.UNDER_REVIEW)

    # UNDER_REVIEW -> APPROVED
    validate_state_transition(NominationStatus.UNDER_REVIEW, NominationStatus.APPROVED)

    # UNDER_REVIEW -> REJECTED
    validate_state_transition(NominationStatus.UNDER_REVIEW, NominationStatus.REJECTED)


def test_invalid_transitions():
    """Verify that illegal state machine transitions raise HTTP 400."""
    # DRAFT -> APPROVED (Cannot jump directly to approved)
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition(NominationStatus.DRAFT, NominationStatus.APPROVED)
    assert exc_info.value.status_code == 400

    # DRAFT -> UNDER_REVIEW
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition(NominationStatus.DRAFT, NominationStatus.UNDER_REVIEW)
    assert exc_info.value.status_code == 400

    # SUBMITTED -> APPROVED (Must start review first)
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition(NominationStatus.SUBMITTED, NominationStatus.APPROVED)
    assert exc_info.value.status_code == 400

    # APPROVED -> REJECTED (Terminal states cannot change)
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition(NominationStatus.APPROVED, NominationStatus.REJECTED)
    assert exc_info.value.status_code == 400

    # REJECTED -> APPROVED (Terminal state cannot change)
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition(NominationStatus.REJECTED, NominationStatus.APPROVED)
    assert exc_info.value.status_code == 400


def test_invalid_status_string():
    """Verify that unrecognized status string raises HTTP 400."""
    with pytest.raises(HTTPException) as exc_info:
        validate_state_transition("NON_EXISTENT_STATE", NominationStatus.APPROVED)
    assert exc_info.value.status_code == 400
