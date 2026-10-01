from typing import List, Optional

from backend.models.technician import Technician
from backend.models.work_order import WorkOrder


def calculate_score(
    technician: Technician,
    work_order: WorkOrder
) -> int:
    """
    Calculate how suitable a technician is for a work order.

    Higher score = better candidate.
    """

    score = 0

    # 1. Skill match
    if technician.can_handle(work_order.category):
        score += 50
    else:
        return -1

    # 2. Availability
    if technician.is_available():
        score += 20
    else:
        return -1

    # 3. Same building
    if technician.building.lower() in work_order.location.lower():
        score += 20

    # 4. Lower workload gets a better score
    score += max(0, 10 - technician.current_jobs * 3)

    return score


def find_best_technician(
    technicians: List[Technician],
    work_order: WorkOrder
) -> Optional[Technician]:
    """
    Find the most suitable available technician.
    """

    best_technician = None
    best_score = -1

    for technician in technicians:
        score = calculate_score(technician, work_order)

        if score > best_score:
            best_score = score
            best_technician = technician

    return best_technician


def assign_work_order(
    technicians: List[Technician],
    work_order: WorkOrder
) -> Optional[Technician]:
    """
    Find and assign the best technician to the work order.
    """

    technician = find_best_technician(
        technicians,
        work_order
    )

    if technician is None:
        return None

    work_order.assign(technician.technician_id)
    technician.assign_job()

    return technician