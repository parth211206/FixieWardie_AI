from dataclasses import dataclass, field
from typing import List


@dataclass
class Technician:
    technician_id: str
    name: str
    skills: List[str]
    building: str
    status: str = "AVAILABLE"
    current_jobs: int = 0
    max_jobs: int = 3

    def is_available(self) -> bool:
        return (
            self.status == "AVAILABLE"
            and self.current_jobs < self.max_jobs
        )

    def can_handle(self, required_skill: str) -> bool:
        return required_skill.lower() in [
            skill.lower() for skill in self.skills
        ]

    def assign_job(self):
        self.current_jobs += 1

        if self.current_jobs >= self.max_jobs:
            self.status = "BUSY"

    def complete_job(self):
        if self.current_jobs > 0:
            self.current_jobs -= 1

        if self.current_jobs < self.max_jobs:
            self.status = "AVAILABLE"