from backend.models.technician import Technician
from backend.models.work_order import WorkOrder
from backend.routing.reassignment import reassign_work_order


def create_work_order():
    return WorkOrder(
        work_order_id="WO-REASSIGN-001",
        complaint_id="C-REASSIGN-001",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )


def test_reassign_to_available_technician():

    old_technician = Technician(
        technician_id="TECH-001",
        name="Rahul",
        skills=["plumbing"],
        building="Hostel A"
    )

    new_technician = Technician(
        technician_id="TECH-002",
        name="Arjun",
        skills=["plumbing"],
        building="Hostel A"
    )

    old_technician.assign_job()

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.escalate()

    assigned = reassign_work_order(
        work_order,
        [
            old_technician,
            new_technician
        ]
    )

    assert assigned is not None
    assert assigned.technician_id == "TECH-002"

    assert work_order.status == "ASSIGNED"
    assert work_order.assigned_to == "TECH-002"

    assert old_technician.current_jobs == 0
    assert new_technician.current_jobs == 1


def test_do_not_reassign_to_same_technician():

    technician = Technician(
        technician_id="TECH-001",
        name="Rahul",
        skills=["plumbing"],
        building="Hostel A"
    )

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.escalate()

    assigned = reassign_work_order(
        work_order,
        [technician]
    )

    assert assigned is None
    assert work_order.status == "ESCALATED"


def test_reassign_only_matching_skill():

    old_technician = Technician(
        technician_id="TECH-001",
        name="Rahul",
        skills=["plumbing"],
        building="Hostel A"
    )

    electrician = Technician(
        technician_id="TECH-002",
        name="Arjun",
        skills=["electrical"],
        building="Hostel A"
    )

    work_order = create_work_order()

    work_order.assign("TECH-001")
    work_order.escalate()

    assigned = reassign_work_order(
        work_order,
        [
            old_technician,
            electrician
        ]
    )

    assert assigned is None
    assert work_order.status == "ESCALATED"