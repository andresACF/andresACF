"""Inferencia de tipo de prenda (+ grasp naive = centro del frame).

Uso:
  python3 infer.py --image foto.jpg --weights checkpoints/dobla_garment.pt
  python3 infer.py --image foto.jpg --json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


ROOT = Path(__file__).resolve().parent


def build_model(num_classes: int) -> nn.Module:
    model = models.mobilenet_v3_small(weights=None)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_classes)
    return model


def load_checkpoint(path: Path, device: torch.device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    classes = ckpt["classes"]
    model = build_model(len(classes))
    model.load_state_dict(ckpt["model_state"])
    model.to(device)
    model.eval()
    img_size = int(ckpt.get("img_size", 224))
    return model, classes, img_size


def predict(image_path: Path, weights: Path) -> dict:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, classes, img_size = load_checkpoint(weights, device)

    tf = transforms.Compose(
        [
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    x = tf(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0]
        conf, idx = probs.max(0)
    tipo = classes[int(idx)]
    # grasp naive: centro (v1). Luego bbox/YOLO lo reemplaza.
    result = {
        "tipo": tipo,
        "confianza": round(float(conf), 4),
        "probs": {c: round(float(probs[i]), 4) for i, c in enumerate(classes)},
        "bbox": [0, 0, w, h],
        "grasp": [w // 2, h // 2],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument(
        "--weights",
        type=Path,
        default=ROOT / "checkpoints" / "dobla_garment.pt",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = predict(args.image, args.weights)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['tipo']} ({result['confianza']:.1%})")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
