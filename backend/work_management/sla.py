from datetime import datetime, timedelta

SLA_MINUTES = {
    "LOW": 60,
    "MEDIUM": 30,
    "HIGH": 15,
    "CRITICAL": 5,
}


def get_sla_minutes(risk_level: str) -> int:
    """
    Return the SLA duration for a risk level.
    """

    risk_level = risk_level.upper()

    if risk_level not in SLA_MINUTES:
        raise ValueError(
            f"Unknown risk level: {risk_level}"
        )

    return SLA_MINUTES[risk_level]


def calculate_deadline(
    created_at: datetime,
    risk_level: str
) -> datetime:
    """
    Calculate the SLA deadline for a work order.
    """

    minutes = get_sla_minutes(risk_level)

    return created_at + timedelta(minutes=minutes)


def is_overdue(
    created_at: datetime,
    risk_level: str,
    current_time: datetime | None = None
) -> bool:
    """
    Check whether the SLA deadline has been exceeded.
    """

    if current_time is None:
        current_time = datetime.now()

    deadline = calculate_deadline(
        created_at,
        risk_level
    )

    return current_time > deadline