from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pathlib import Path
import shutil
import uuid

from .intake_agent import IntakeAgent
from .schemas import ComplaintInput


app = FastAPI(
    title="ARIA Member 1 API",
    description="AI Intake, Triage and Evidence Analysis",
    version="1.0.0"
)


agent = IntakeAgent()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "ARIA Member 1 API is running"
    }


@app.post("/analyze")
async def analyze_complaint(
    description: str = Form(...),
    category: str | None = Form(None),
    location: str | None = Form(None),
    image: UploadFile | None = File(None)
):

    image_path = None

    # Handle uploaded image
    if image is not None:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG and WEBP images are supported."
            )

        file_name = f"{uuid.uuid4()}_{image.filename}"

        image_path = UPLOAD_DIR / file_name

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # Create complaint object
    complaint = ComplaintInput(
        description=description,
        category=category,
        location=location
    )

    # Run Member 1 pipeline
    result = agent.analyze(
        complaint=complaint,
        image_path=str(image_path) if image_path else None
    )

    return result