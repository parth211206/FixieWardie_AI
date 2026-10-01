from datetime import datetime

from backend.models.work_order import WorkOrder
from backend.work_management.sla import is_overdue


def check_and_escalate(
    work_order: WorkOrder,
    current_time: datetime | None = None
) -> bool:
    """
    Check whether a work order has exceeded its SLA.

    Returns:
        True  -> escalation happened
        False -> no escalation needed
    """

    if work_order.status in {"RESOLVED", "CLOSED"}:
        return False

    if is_overdue(
        work_order.created_at,
        work_order.risk_level,
        current_time
    ):
        work_order.escalate()
        return True

    return False