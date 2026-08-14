from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


# =========================
# 1. Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "dataset" / "chest_xray"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# 2. Device
# =========================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")


# =========================
# 3. Image transformations
# =========================

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


# =========================
# 4. Load datasets
# =========================

train_dataset = datasets.ImageFolder(
    DATA_DIR / "train",
    transform=train_transform,
)

val_dataset = datasets.ImageFolder(
    DATA_DIR / "val",
    transform=test_transform,
)

test_dataset = datasets.ImageFolder(
    DATA_DIR / "test",
    transform=test_transform,
)


print(f"Classes: {train_dataset.classes}")
print(f"Training images: {len(train_dataset)}")
print(f"Validation images: {len(val_dataset)}")
print(f"Testing images: {len(test_dataset)}")


# =========================
# 5. Data loaders
# =========================

train_loader = DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=0,
)

val_loader = DataLoader(
    val_dataset,
    batch_size=16,
    shuffle=False,
    num_workers=0,
)

test_loader = DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=False,
    num_workers=0,
)


# =========================
# 6. Load ResNet18
# =========================

print("\nLoading ResNet18...")

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Replace final layer for 2 classes:
# NORMAL / PNEUMONIA

model.fc = nn.Linear(
    model.fc.in_features,
    2,
)

model = model.to(device)


# =========================
# 7. Loss and optimizer
# =========================

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.0001,
)


# =========================
# 8. Training
# =========================

EPOCHS = 3

best_val_accuracy = 0.0

model_path = MODEL_DIR / "chest_xray_resnet18.pth"


for epoch in range(EPOCHS):

    print(f"\nEpoch {epoch + 1}/{EPOCHS}")
    print("-" * 40)

    # ---------------------
    # Training
    # ---------------------

    model.train()

    train_correct = 0
    train_total = 0
    train_loss = 0.0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

        _, predicted = torch.max(outputs, 1)

        train_total += labels.size(0)
        train_correct += (predicted == labels).sum().item()

    train_accuracy = 100 * train_correct / train_total

    # ---------------------
    # Validation
    # ---------------------

    model.eval()

    val_correct = 0
    val_total = 0

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    val_accuracy = 100 * val_correct / val_total

    print(
        f"Loss: {train_loss / len(train_loader):.4f}"
    )

    print(
        f"Training Accuracy: {train_accuracy:.2f}%"
    )

    print(
        f"Validation Accuracy: {val_accuracy:.2f}%"
    )

    # Save best model

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = val_accuracy

        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "classes": train_dataset.classes,
            },
            model_path,
        )

        print("Best model saved!")


# =========================
# 9. Load best model
# =========================

print("\nLoading best model...")

checkpoint = torch.load(
    model_path,
    map_location=device,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.eval()


# =========================
# 10. Test
# =========================

test_correct = 0
test_total = 0

with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)

        _, predicted = torch.max(outputs, 1)

        test_total += labels.size(0)
        test_correct += (predicted == labels).sum().item()


test_accuracy = 100 * test_correct / test_total


# =========================
# 11. Final result
# =========================

print("\n" + "=" * 50)

print(
    f"Test Accuracy: {test_accuracy:.2f}%"
)

print(
    f"Model saved at: {model_path}"
)

print("Training completed successfully!")

print("=" * 50)