from typing import Any

from backend.app.ai.base.base_model import BaseMedicalImageModel
from backend.app.ai.chest.pneumonia_model import ChestPneumoniaModel


class MedicalModelRegistry:
    """
    Central registry for all medical imaging AI models.

    New models can be registered here without changing
    the rest of the application.
    """

    def __init__(self):
        self._models: dict[str, BaseMedicalImageModel] = {}

        # Register currently available model
        self.register(
            "chest_pneumonia",
            ChestPneumoniaModel(),
        )

    def register(
        self,
        name: str,
        model: BaseMedicalImageModel,
    ) -> None:
        """
        Register an AI model.
        """

        self._models[name] = model

    def get(
        self,
        name: str,
    ) -> BaseMedicalImageModel:
        """
        Get a registered model by name.
        """

        if name not in self._models:
            raise ValueError(
                f"AI model not registered: {name}"
            )

        return self._models[name]

    def list_models(self) -> list[dict[str, Any]]:
        """
        Return information about all registered models.
        """

        return [
            {
                "name": name,
                **model.get_model_info(),
            }
            for name, model in self._models.items()
        ]


# Global model registry
model_registry = MedicalModelRegistry()