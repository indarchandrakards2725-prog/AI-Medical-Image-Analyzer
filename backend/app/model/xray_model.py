from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms


class XRayModel:
    """
    X-ray model wrapper.

    Current version only loads and preprocesses the image.
    It does not independently diagnose medical conditions.
    """

    def __init__(self):
        self.device = torch.device("cpu")
        self.model = None

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    def load_image(self, image_path: str) -> Image.Image:
        file_path = Path(image_path)

        if not file_path.exists():
            raise FileNotFoundError("X-ray image file not found")

        if not file_path.is_file():
            raise ValueError("Invalid X-ray image path")

        return Image.open(file_path).convert("RGB")

    def preprocess(self, image_path: str) -> torch.Tensor:
        image = self.load_image(image_path)

        tensor = self.transform(image)

        # Add batch dimension
        tensor = tensor.unsqueeze(0)

        return tensor.to(self.device)

    def predict(self, image_path: str) -> dict:
        image = self.load_image(image_path)
        tensor = self.preprocess(image_path)

        return {
            "status": "pending",
            "message": "Image preprocessing completed. Model weights are not connected yet.",
            "image_size": image.size,
            "tensor_shape": list(tensor.shape),
        }


xray_model = XRayModel()