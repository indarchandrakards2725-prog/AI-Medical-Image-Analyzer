from typing import Any

from backend.app.ai.registry.model_registry import model_registry


class AIRouter:
    """
    Routes medical images to the appropriate AI model.
    """

    def analyze(
        self,
        image_path: str,
        model_name: str,
    ) -> dict[str, Any]:
        """
        Analyze an image using a registered AI model.
        """

        model = model_registry.get(model_name)

        result = model.predict(image_path)

        return {
            **result,
            "requested_model": model_name,
        }

    def available_models(self) -> list[dict[str, Any]]:
        """
        Return all available AI models.
        """

        return model_registry.list_models()


ai_router = AIRouter()