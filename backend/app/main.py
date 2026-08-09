from fastapi import FastAPI

from backend.app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Research prototype for doctor-reviewed adult chest X-ray analysis. "
        "It must not be used for independent diagnosis."
    ),
    debug=settings.app_debug,
)


@app.get("/", tags=["System"])
def health_check() -> dict[str, str]:
    """Confirm that the backend is running."""

    return {
        "status": "ok",
        "application": settings.app_name,
        "environment": settings.app_env,
        "safety_notice": "Research use only. Doctor approval is required.",
    }


@app.get("/api/v1/intended-use", tags=["System"])
def intended_use() -> dict[str, str]:
    """Expose the prototype's intended use and its safety limitation."""

    return {
        "intended_use": (
            "Assist qualified doctors in reviewing signs associated with "
            "pneumonia on adult chest X-rays."
        ),
        "limitation": (
            "The application does not independently diagnose patients, and "
            "patients must not receive unapproved AI output."
        ),
    }

