from datetime import datetime
from datetime import timedelta

from backend.intelligence.complaint_processor import process_complaint
from backend.routing.router import route_work_order
from backend.routing.escalation import check_and_escalate
from backend.routing.reassignment import reassign_work_order
from backend.models.technician import Technician


def test_full_work_order_lifecycle():

    # 1. Complaint enters the system
    work_order = process_complaint(
        complaint_id="C-200",
        complaint_text="Water is leaking badly from the bathroom pipe",
        location="Hostel A - Floor 3",
    )

    assert work_order.category == "plumbing"
    assert work_order.risk_level == "HIGH"
    assert work_order.status == "CREATED"

    # 2. Technicians
    technicians = [
        Technician(
            technician_id="TECH-001",
            name="Rahul",
            skills=["plumbing"],
            building="Hostel A",
        ),
        Technician(
            technician_id="TECH-002",
            name="Amit",
            skills=["plumbing"],
            building="Hostel A",
        ),
    ]

    # 3. Initial assignment
    assigned = route_work_order(
        work_order,
        technicians,
    )

    assert assigned is not None
    assert work_order.status == "ASSIGNED"

    original_technician = work_order.assigned_to

    # 4. Simulate SLA breach
    future_time = work_order.created_at + timedelta(minutes=16)

    escalated = check_and_escalate(
        work_order,
        future_time,
    )

    assert escalated is True
    assert work_order.status == "ESCALATED"
    assert work_order.escalation_count == 1

    # 5. Reassign to another technician
    new_technician = reassign_work_order(
        work_order,
        technicians,
    )

    assert new_technician is not None
    assert new_technician.technician_id != original_technician
    assert work_order.status == "ASSIGNED"
    assert work_order.assigned_to == new_technician.technician_id