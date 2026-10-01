import pytest

from backend.work_management.state_machine import (
    transition,
    InvalidTransitionError
)


def test_valid_transitions():

    assert transition("CREATED", "ASSIGNED") == "ASSIGNED"

    assert transition(
        "ASSIGNED",
        "ACKNOWLEDGED"
    ) == "ACKNOWLEDGED"

    assert transition(
        "ACKNOWLEDGED",
        "IN_PROGRESS"
    ) == "IN_PROGRESS"

    assert transition(
        "IN_PROGRESS",
        "RESOLVED"
    ) == "RESOLVED"

    assert transition(
        "RESOLVED",
        "CLOSED"
    ) == "CLOSED"


def test_escalation_transition():

    assert transition(
        "ASSIGNED",
        "ESCALATED"
    ) == "ESCALATED"

    assert transition(
        "IN_PROGRESS",
        "ESCALATED"
    ) == "ESCALATED"


def test_invalid_transition():

    with pytest.raises(InvalidTransitionError):
        transition(
            "CREATED",
            "RESOLVED"
        )


def test_closed_cannot_change():

    with pytest.raises(InvalidTransitionError):
        transition(
            "CLOSED",
            "ASSIGNED"
        )