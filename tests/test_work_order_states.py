import pytest

from backend.models.work_order import WorkOrder
from backend.work_management.state_machine import (
    InvalidTransitionError
)


def create_work_order():
    return WorkOrder(
        work_order_id="WO-TEST",
        complaint_id="C-TEST",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )


def test_complete_workflow():

    work_order = create_work_order()

    assert work_order.status == "CREATED"

    work_order.assign("TECH-001")
    assert work_order.status == "ASSIGNED"

    work_order.acknowledge()
    assert work_order.status == "ACKNOWLEDGED"

    work_order.start()
    assert work_order.status == "IN_PROGRESS"

    work_order.resolve()
    assert work_order.status == "RESOLVED"

    work_order.close()
    assert work_order.status == "CLOSED"


def test_invalid_workflow():

    work_order = create_work_order()

    with pytest.raises(InvalidTransitionError):
        work_order.resolve()


def test_escalation():

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.escalate()

    assert work_order.status == "ESCALATED"
    assert work_order.escalation_count == 1


def test_closed_work_order_cannot_change():

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.acknowledge()
    work_order.start()
    work_order.resolve()
    work_order.close()

    with pytest.raises(InvalidTransitionError):
        work_order.assign("TECH-002")