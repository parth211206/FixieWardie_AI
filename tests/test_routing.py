from backend.models.technician import Technician
from backend.models.work_order import WorkOrder
from backend.routing.assignment import (
    find_best_technician,
    assign_work_order
)


def test_technician():
    technician = Technician(
        technician_id="TECH-001",
        name="Rahul",
        skills=["plumbing"],
        building="Hostel A"
    )

    assert technician.is_available()
    assert technician.can_handle("plumbing")


def test_work_order():
    work_order = WorkOrder(
        work_order_id="WO-001",
        complaint_id="C-001",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )

    assert work_order.status == "CREATED"

    work_order.assign("TECH-001")

    assert work_order.status == "ASSIGNED"
    assert work_order.assigned_to == "TECH-001"


def test_find_best_technician():

    technicians = [
        Technician(
            technician_id="TECH-001",
            name="Rahul",
            skills=["plumbing"],
            building="Hostel A"
        ),

        Technician(
            technician_id="TECH-002",
            name="Arjun",
            skills=["plumbing"],
            building="Hostel B",
            current_jobs=2
        ),

        Technician(
            technician_id="TECH-003",
            name="Vikram",
            skills=["electrical"],
            building="Hostel A"
        )
    ]

    work_order = WorkOrder(
        work_order_id="WO-002",
        complaint_id="C-002",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )

    best = find_best_technician(
        technicians,
        work_order
    )

    assert best is not None
    assert best.technician_id == "TECH-001"


def test_assign_work_order():

    technicians = [
        Technician(
            technician_id="TECH-001",
            name="Rahul",
            skills=["plumbing"],
            building="Hostel A"
        )
    ]

    work_order = WorkOrder(
        work_order_id="WO-003",
        complaint_id="C-003",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 2"
    )

    assigned = assign_work_order(
        technicians,
        work_order
    )

    assert assigned is not None
    assert assigned.technician_id == "TECH-001"

    assert work_order.status == "ASSIGNED"
    assert work_order.assigned_to == "TECH-001"

    assert assigned.current_jobs == 1
from backend.routing.router import route_work_order


def test_route_work_order():

    technicians = [
        Technician(
            technician_id="TECH-001",
            name="Rahul",
            skills=["plumbing"],
            building="Hostel A"
        ),
        Technician(
            technician_id="TECH-002",
            name="Arjun",
            skills=["electrical"],
            building="Hostel A"
        )
    ]

    work_order = WorkOrder(
        work_order_id="WO-004",
        complaint_id="C-004",
        category="plumbing",
        risk_level="HIGH",
        location="Hostel A - Floor 3"
    )

    assigned = route_work_order(
        work_order,
        technicians
    )

    assert assigned is not None
    assert assigned.technician_id == "TECH-001"
    assert work_order.status == "ASSIGNED"