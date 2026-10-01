from typing import List

from backend.models.technician import Technician
from backend.models.work_order import WorkOrder
from backend.routing.assignment import assign_work_order


def route_work_order(
    work_order: WorkOrder,
    technicians: List[Technician]
):
    """
    Route a work order to the most suitable technician.
    """

    if work_order.status != "CREATED":
        raise ValueError(
            "Only CREATED work orders can be routed."
        )

    technician = assign_work_order(
        technicians,
        work_order
    )

    return technician