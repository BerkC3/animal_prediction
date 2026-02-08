"""Backend module for animal classification using ResNet18."""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from typing import Dict
import os

try:
    import pillow_avif
except ImportError:
    pass

CLASS_NAMES = [
    "antelope", "bat", "beaver", "blue whale", "bobcat", "buffalo",
    "chihuahua", "chimpanzee", "collie", "cow", "dalmatian", "deer",
    "dolphin", "elephant", "fox", "german shepherd", "giant panda",
    "giraffe", "gorilla", "grizzly bear", "hamster", "hippopotamus",
    "horse", "humpback whale", "killer whale", "leopard", "lion",
    "mole", "moose", "mouse", "otter", "ox", "persian cat", "pig",
    "polar bear", "rabbit", "raccoon", "rat", "rhinoceros", "seal",
    "sheep", "siamese cat", "skunk", "spider monkey", "squirrel",
    "tiger", "walrus", "weasel", "wolf", "zebra"
]


class Predictor:
    """Image classifier for 50 animal species using ResNet18."""

    def __init__(self, model_path: str = "ResNet18_Animals_Best_Acc87.38.pth"):
        self.device = self._get_device()
        self.class_names = CLASS_NAMES
        self.model = self._load_model(model_path)
        self.transform = self._get_transforms()
        print(f"[OK] Model loaded on {self.device}")

    def _get_device(self) -> torch.device:
        if torch.cuda.is_available():
            print(f"[OK] GPU: {torch.cuda.get_device_name(0)}")
            return torch.device("cuda")
        print("[INFO] Using CPU")
        return torch.device("cpu")

    def _load_model(self, model_path: str) -> nn.Module:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        state_dict = torch.load(model_path, map_location=self.device)
        num_classes = state_dict['fc.weight'].shape[0]

        if num_classes != len(CLASS_NAMES):
            extended = CLASS_NAMES.copy()
            for i in range(len(CLASS_NAMES), num_classes):
                extended.append(f"class_{i+1}")
            self.class_names = extended

        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        model.load_state_dict(state_dict)
        model.eval()
        model.to(self.device)
        return model

    def _get_transforms(self) -> transforms.Compose:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image: Image.Image) -> Dict[str, float]:
        if image.mode != 'RGB':
            image = image.convert('RGB')

        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)

        results = {self.class_names[i]: float(probs[i]) for i in range(len(self.class_names))}
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    def get_top_predictions(self, image: Image.Image, top_k: int = 3) -> Dict[str, float]:
        predictions = self.predict(image)
        return dict(list(predictions.items())[:top_k])


if __name__ == "__main__":
    try:
        p = Predictor()
        print(f"[OK] Classes: {len(p.class_names)}")
    except Exception as e:
        print(f"[ERROR] {e}")
