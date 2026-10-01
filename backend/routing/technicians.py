from backend.models.technician import Technician


TECHNICIANS = [
    Technician(
        technician_id="TECH-001",
        name="Arjun",
        skills=["plumbing", "electrical"],
        building="Hostel A",
        status="AVAILABLE",
        current_jobs=0,
        max_jobs=3,
    ),
    Technician(
        technician_id="TECH-002",
        name="Rahul",
        skills=["electrical", "plumbing"],
        building="Hostel B",
        status="AVAILABLE",
        current_jobs=0,
        max_jobs=3,
    ),
]


def get_technicians():
    return TECHNICIANS