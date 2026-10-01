class InvalidTransitionError(Exception):
    """Raised when a work order attempts an invalid status transition."""
    pass


VALID_TRANSITIONS = {
    "CREATED": {"ASSIGNED"},
    "ASSIGNED": {"ACKNOWLEDGED", "ESCALATED"},
    "ACKNOWLEDGED": {"IN_PROGRESS", "ESCALATED"},
    "IN_PROGRESS": {"RESOLVED", "ESCALATED"},
    "ESCALATED": {"ASSIGNED"},
    "RESOLVED": {"CLOSED"},
    "CLOSED": set(),
}


def transition(current_status: str, new_status: str) -> str:
    """
    Validate and return a new work-order status.
    """

    allowed_states = VALID_TRANSITIONS.get(current_status, set())

    if new_status not in allowed_states:
        raise InvalidTransitionError(
            f"Cannot transition from {current_status} to {new_status}"
        )

    return new_status