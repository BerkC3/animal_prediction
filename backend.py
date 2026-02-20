"""Backend module for animal classification using ResNet18."""

import torch
import torch.nn as nn
import numpy as np
import cv2
from torchvision import models, transforms
from PIL import Image
from typing import Dict, Tuple
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

    def generate_gradcam(self, image: Image.Image) -> Tuple[Dict[str, float], Image.Image]:
        if image.mode != 'RGB':
            image = image.convert('RGB')

        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        gradients = []
        activations = []

        def save_gradient(grad):
            gradients.append(grad)

        def hook_fn(module, input, output):
            activations.append(output)
            output.register_hook(save_gradient)

        handle = self.model.layer4.register_forward_hook(hook_fn)

        outputs = self.model(input_tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
        top_class = probs.argmax().item()

        self.model.zero_grad()
        outputs[0, top_class].backward()

        handle.remove()

        probs = probs.detach()

        grads = gradients[0].cpu().detach().numpy()[0]      # (C, H, W)
        acts = activations[0].cpu().detach().numpy()[0]     # (C, H, W)

        weights = grads.mean(axis=(1, 2))                   # (C,)
        cam = np.sum(weights[:, None, None] * acts, axis=0) # (H, W)
        cam = np.maximum(cam, 0)
        cam = cam / (cam.max() + 1e-8)

        orig_w, orig_h = image.size
        cam_resized = cv2.resize(cam, (orig_w, orig_h))
        heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

        orig_np = np.array(image)
        overlay = (0.5 * orig_np + 0.5 * heatmap).astype(np.uint8)
        result_image = Image.fromarray(overlay)

        all_preds = {self.class_names[i]: float(probs[i]) for i in range(len(self.class_names))}
        top5 = dict(sorted(all_preds.items(), key=lambda x: x[1], reverse=True)[:5])

        return top5, result_image


if __name__ == "__main__":
    try:
        p = Predictor()
        print(f"[OK] Classes: {len(p.class_names)}")
    except Exception as e:
        print(f"[ERROR] {e}")
