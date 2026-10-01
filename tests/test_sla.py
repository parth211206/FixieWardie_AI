from datetime import datetime, timedelta

import pytest

from backend.work_management.sla import (
    get_sla_minutes,
    calculate_deadline,
    is_overdue,
)


def test_sla_duration():

    assert get_sla_minutes("LOW") == 60
    assert get_sla_minutes("MEDIUM") == 30
    assert get_sla_minutes("HIGH") == 15
    assert get_sla_minutes("CRITICAL") == 5


def test_invalid_risk_level():

    with pytest.raises(ValueError):
        get_sla_minutes("UNKNOWN")


def test_calculate_deadline():

    created_at = datetime(2026, 10, 1, 10, 0, 0)

    deadline = calculate_deadline(
        created_at,
        "HIGH"
    )

    assert deadline == datetime(
        2026, 10, 1, 10, 15, 0
    )


def test_overdue():

    created_at = datetime(
        2026, 10, 1, 10, 0, 0
    )

    current_time = datetime(
        2026, 10, 1, 10, 16, 0
    )

    assert is_overdue(
        created_at,
        "HIGH",
        current_time
    )


def test_not_overdue():

    created_at = datetime(
        2026, 10, 1, 10, 0, 0
    )

    current_time = datetime(
        2026, 10, 1, 10, 10, 0
    )

    assert not is_overdue(
        created_at,
        "HIGH",
        current_time
    )