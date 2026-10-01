from datetime import datetime

from backend.models.work_order import WorkOrder
from backend.routing.escalation import check_and_escalate


def create_work_order():
    return WorkOrder(
        work_order_id="WO-ESC-001",
        complaint_id="C-ESC-001",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )


def test_overdue_work_order_escalates():

    work_order = create_work_order()

    work_order.created_at = datetime(
        2026,
        10,
        1,
        10,
        0
    )

    work_order.assign("TECH-001")

    current_time = datetime(
        2026,
        10,
        1,
        10,
        16
    )

    result = check_and_escalate(
        work_order,
        current_time
    )

    assert result is True
    assert work_order.status == "ESCALATED"
    assert work_order.escalation_count == 1


def test_work_order_not_overdue():

    work_order = create_work_order()

    work_order.assign("TECH-001")

    current_time = datetime(
        2026,
        10,
        1,
        10,
        10
    )

    result = check_and_escalate(
        work_order,
        current_time
    )

    assert result is False
    assert work_order.status == "ASSIGNED"
    assert work_order.escalation_count == 0


def test_resolved_work_order_does_not_escalate():

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.acknowledge()
    work_order.start()
    work_order.resolve()

    current_time = datetime(
        2026,
        10,
        1,
        11,
        0
    )

    result = check_and_escalate(
        work_order,
        current_time
    )

    assert result is False
    assert work_order.status == "RESOLVED"
    assert work_order.escalation_count == 0