from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


class XRayModel:
    """
    X-ray model wrapper.

    Uses a trained ResNet18 model to classify chest X-ray images
    into NORMAL or PNEUMONIA.

    This prototype is for project/testing purposes and does not
    independently diagnose medical conditions.
    """

    def __init__(self):
        # Use CPU
        self.device = torch.device("cpu")

        # Project root:
        # AI-Medical-Image-Analyzer-main
        PROJECT_ROOT = Path(__file__).resolve().parents[3]

        # Trained model path
        self.model_path = (
            PROJECT_ROOT
            / "training"
            / "models"
            / "chest_xray_resnet18.pth"
        )

        # Class names used during training
        self.classes = ["NORMAL", "PNEUMONIA"]

        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

        # Load trained model
        self.model = self._load_model()

    def _load_model(self):
        """Load trained ResNet18 model."""

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Trained model not found at: {self.model_path}"
            )

        # Create ResNet18 architecture
        model = models.resnet18(weights=None)

        # Our model has 2 classes:
        # NORMAL and PNEUMONIA
        model.fc = nn.Linear(
            model.fc.in_features,
            2,
        )

        # Load saved checkpoint
        checkpoint = torch.load(
            self.model_path,
            map_location=self.device,
        )

        # Our training script saved a dictionary
        # containing model_state_dict and classes
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            model.load_state_dict(
                checkpoint["model_state_dict"]
            )

            # Use classes saved during training if available
            if "classes" in checkpoint:
                self.classes = checkpoint["classes"]

        else:
            # Support a plain state_dict as well
            model.load_state_dict(checkpoint)

        model.to(self.device)

        # Evaluation mode
        model.eval()

        print(f"X-ray model loaded successfully from: {self.model_path}")

        return model

    def load_image(self, image_path: str) -> Image.Image:
        """Load X-ray image."""

        file_path = Path(image_path)

        if not file_path.exists():
            raise FileNotFoundError(
                "X-ray image file not found"
            )

        if not file_path.is_file():
            raise ValueError(
                "Invalid X-ray image path"
            )

        return Image.open(file_path).convert("RGB")

    def preprocess(self, image_path: str) -> torch.Tensor:
        """Preprocess image for the model."""

        image = self.load_image(image_path)

        tensor = self.transform(image)

        # Add batch dimension
        tensor = tensor.unsqueeze(0)

        return tensor.to(self.device)

    def predict(self, image_path: str) -> dict:
        """Run X-ray classification."""

        image = self.load_image(image_path)

        tensor = self.preprocess(image_path)

        # Run model prediction
        with torch.no_grad():
            outputs = self.model(tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )

            confidence, predicted_index = torch.max(
                probabilities,
                dim=1,
            )

        predicted_index = predicted_index.item()
        confidence = confidence.item()

        predicted_class = self.classes[predicted_index]

        # Probability for each class
        normal_probability = probabilities[0][0].item()
        pneumonia_probability = probabilities[0][1].item()

        return {
            "status": "success",
            "message": "X-ray image analyzed successfully",
            "prediction": predicted_class,
            "confidence": round(
                confidence * 100,
                2,
            ),
            "probabilities": {
                "NORMAL": round(
                    normal_probability * 100,
                    2,
                ),
                "PNEUMONIA": round(
                    pneumonia_probability * 100,
                    2,
                ),
            },
            "image_size": image.size,
            "model": "ResNet18",
        }


# Create global model instance
xray_model = XRayModel()