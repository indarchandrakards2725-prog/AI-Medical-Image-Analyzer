from pathlib import Path

from backend.app.model.xray_model import xray_model


def analyze_xray(image_path: str) -> dict:
    """
    Run the X-ray analysis pipeline.

    The current model is a prototype and does not independently
    diagnose medical conditions.
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
        result = xray_model.predict(str(file_path))

        return {
            "status": "success",
            "message": "X-ray image processed successfully",
            "filename": file_path.name,
            "analysis": result,
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }