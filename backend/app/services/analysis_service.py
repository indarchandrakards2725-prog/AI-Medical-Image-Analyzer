from pathlib import Path

from backend.app.ai.router.ai_router import ai_router


def analyze_xray(
    image_path: str,
    model_name: str = "chest_pneumonia",
) -> dict:
    """
    Run the medical X-ray analysis pipeline.

    The requested AI model is selected through the AI router.
    The current chest model is intended for AI-assisted screening
    and does not independently diagnose medical conditions.
    """

    file_path = Path(image_path)

    if not file_path.exists():
        return {
            "status": "error",
            "message": "X-ray image file not found",
        }

    if not file_path.is_file():
        return {
            "status": "error",
            "message": "Invalid X-ray image path",
        }

    try:
        result = ai_router.analyze(
            image_path=str(file_path),
            model_name=model_name,
        )

        return {
            "status": "success",
            "message": "X-ray image processed successfully",
            "filename": file_path.name,
            "model_name": model_name,
            "analysis": result,
        }

    except ValueError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": f"AI analysis failed: {exc}",
        }