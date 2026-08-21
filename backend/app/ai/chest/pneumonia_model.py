from typing import Any

from backend.app.ai.base.base_model import BaseMedicalImageModel
from backend.app.model.xray_model import XRayModel


class ChestPneumoniaModel(BaseMedicalImageModel):
    """
    Adapter for the existing Chest X-ray ResNet18 model.

    The existing XRayModel remains unchanged.
    This class exposes it through the new scalable AI architecture.
    """

    model_name = "chest_pneumonia"
    modality = "xray"

    def __init__(self):
        self.model = XRayModel()

    def load(self) -> None:
        """
        The existing XRayModel loads its weights during initialization.
        """
        return None

    def predict(self, image_path: str) -> dict[str, Any]:
        """
        Run the existing Chest X-ray pneumonia model.
        """

        self.validate_image_path(image_path)

        result = self.model.predict(image_path)

        return {
            **result,
            "model_name": self.model_name,
            "modality": self.modality,
            "body_region": "chest",
        }