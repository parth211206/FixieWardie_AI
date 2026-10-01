from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="FixieWardie Incident Intelligence API",
    description=(
        "AI-assisted complaint prioritization, "
        "correlation, incident clustering and risk analysis."
    ),
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "FixieWardie Incident Intelligence API",
        "status": "running",
        "docs": "/docs",
    }
