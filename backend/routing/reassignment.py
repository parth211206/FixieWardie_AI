from typing import List, Optional

from backend.models.technician import Technician
from backend.models.work_order import WorkOrder


def reassign_work_order(
    work_order: WorkOrder,
    technicians: List[Technician]
) -> Optional[Technician]:
    """
    Reassign an escalated work order to another suitable technician.
    """

    if work_order.status != "ESCALATED":
        return None

    old_technician_id = work_order.assigned_to

    candidates = []

    for technician in technicians:

        # Do not reassign to the same technician
        if technician.technician_id == old_technician_id:
            continue

        # Technician must be available
        if not technician.is_available():
            continue

        # Technician must have the required skill
        if not technician.can_handle(work_order.category):
            continue

        candidates.append(technician)

    if not candidates:
        return None

    # Pick the technician with the lowest workload
    new_technician = min(
        candidates,
        key=lambda technician: technician.current_jobs
    )

    # Release old technician's workload
    for technician in technicians:
        if technician.technician_id == old_technician_id:
            if technician.current_jobs > 0:
                technician.current_jobs -= 1

    # ESCALATED → ASSIGNED
    work_order.status = "ASSIGNED"
    work_order.assigned_to = new_technician.technician_id
    work_order.assigned_at = __import__("datetime").datetime.now()

    new_technician.assign_job()

    return new_technician