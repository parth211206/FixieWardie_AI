from datetime import datetime

from backend.work_management.state_machine import transition


class WorkOrder:
    def __init__(
        self,
        work_order_id: str,
        complaint_id: str,
        category: str,
        risk_level: str,
        location: str,
    ):
        self.work_order_id = work_order_id
        self.complaint_id = complaint_id
        self.category = category
        self.risk_level = risk_level
        self.location = location

        # Initial state
        self.status = "CREATED"

        # Assignment information
        self.assigned_to = None
        self.assigned_at = None

        # Lifecycle timestamps
        self.created_at = datetime.now()
        self.acknowledged_at = None
        self.started_at = None
        self.resolved_at = None
        self.closed_at = None

        # Escalation tracking
        self.escalation_count = 0

    def assign(self, technician_id: str):
        self.status = transition(
            self.status,
            "ASSIGNED"
        )
        self.assigned_to = technician_id
        self.assigned_at = datetime.now()

    def acknowledge(self):
        self.status = transition(
            self.status,
            "ACKNOWLEDGED"
        )
        self.acknowledged_at = datetime.now()

    def start(self):
        self.status = transition(
            self.status,
            "IN_PROGRESS"
        )
        self.started_at = datetime.now()

    def resolve(self):
        self.status = transition(
            self.status,
            "RESOLVED"
        )
        self.resolved_at = datetime.now()

    def close(self):
        self.status = transition(
            self.status,
            "CLOSED"
        )
        self.closed_at = datetime.now()

    def escalate(self):
        self.status = transition(
            self.status,
            "ESCALATED"
        )
        self.escalation_count += 1

    def reassign(self, technician_id: str):
        self.status = transition(
            self.status,
            "ASSIGNED"
        )
        self.assigned_to = technician_id
        self.assigned_at = datetime.now()