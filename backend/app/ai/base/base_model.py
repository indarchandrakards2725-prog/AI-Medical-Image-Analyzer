from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseMedicalImageModel(ABC):
    """
    Base interface for all medical X-ray AI models.

    Every modality-specific model (chest, bone, dental, etc.)
    must implement this interface.
    """

    model_name: str = "unknown"
    modality: str = "unknown"

    @abstractmethod
    def load(self) -> None:
        """
        Load model weights into memory.
        """
        pass

    @abstractmethod
    def predict(self, image_path: str) -> dict[str, Any]:
        """
        Analyze an image and return a standardized result.
        """
        pass

    def validate_image_path(self, image_path: str) -> Path:
        """
        Validate that the supplied image exists and is a file.
        """

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Medical image not found: {image_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Invalid medical image path: {image_path}"
            )

        return path

    def get_model_info(self) -> dict[str, str]:
        """
        Return basic information about the AI model.
        """

        return {
            "model_name": self.model_name,
            "modality": self.modality,
        }