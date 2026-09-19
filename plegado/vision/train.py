"""Entrena clasificador RGB de prendas (MobileNetV3).

Uso:
  python3 train.py --data data --epochs 8 --out checkpoints/dobla_garment.pt
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from tqdm import tqdm


ROOT = Path(__file__).resolve().parent


def build_model(num_classes: int) -> nn.Module:
    weights = models.MobileNet_V3_Small_Weights.DEFAULT
    model = models.mobilenet_v3_small(weights=weights)
    in_features = model.classifier[-1].in_features
    model.classifier[-1] = nn.Linear(in_features, num_classes)
    return model


def accuracy(logits: torch.Tensor, y: torch.Tensor) -> float:
    pred = logits.argmax(dim=1)
    return (pred == y).float().mean().item()


def run_epoch(model, loader, criterion, optimizer, device, train: bool):
    model.train(train)
    total_loss, total_acc, n = 0.0, 0.0, 0
    ctx = torch.enable_grad() if train else torch.no_grad()
    with ctx:
        for x, y in tqdm(loader, leave=False):
            x, y = x.to(device), y.to(device)
            if train:
                optimizer.zero_grad(set_to_none=True)
            logits = model(x)
            loss = criterion(logits, y)
            if train:
                loss.backward()
                optimizer.step()
            bs = x.size(0)
            total_loss += loss.item() * bs
            total_acc += accuracy(logits, y) * bs
            n += bs
    return total_loss / max(n, 1), total_acc / max(n, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--out", type=Path, default=ROOT / "checkpoints" / "dobla_garment.pt")
    parser.add_argument("--img-size", type=int, default=224)
    args = parser.parse_args()

    classes_meta = json.loads((ROOT / "classes.json").read_text(encoding="utf-8"))
    class_names = classes_meta["classes"]

    train_tf = transforms.Compose(
        [
            transforms.Resize((args.img_size, args.img_size)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(25),
            transforms.ColorJitter(0.25, 0.25, 0.2, 0.05),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    val_tf = transforms.Compose(
        [
            transforms.Resize((args.img_size, args.img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    train_ds = datasets.ImageFolder(args.data / "train", transform=train_tf)
    val_ds = datasets.ImageFolder(args.data / "val", transform=val_tf)

    # Forzar orden de classes.json (ImageFolder ordena alfabético por defecto)
    class_to_idx = {name: i for i, name in enumerate(class_names)}
    missing = [c for c in class_names if c not in train_ds.class_to_idx]
    if missing:
        raise SystemExit(f"Faltan carpetas en data/train: {missing}")

    def remapped(ds):
        samples = []
        for path, _ in ds.samples:
            label_name = Path(path).parent.name
            samples.append((path, class_to_idx[label_name]))
        ds.samples = samples
        ds.targets = [s[1] for s in samples]
        ds.classes = list(class_names)
        ds.class_to_idx = class_to_idx
        return ds

    train_ds = remapped(train_ds)
    val_ds = remapped(val_ds)

    train_loader = DataLoader(
        train_ds, batch_size=args.batch_size, shuffle=True, num_workers=2
    )
    val_loader = DataLoader(
        val_ds, batch_size=args.batch_size, shuffle=False, num_workers=2
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model(len(train_ds.classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    best_acc = -1.0
    history = []
    args.out.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = run_epoch(
            model, train_loader, criterion, optimizer, device, train=True
        )
        va_loss, va_acc = run_epoch(
            model, val_loader, criterion, optimizer, device, train=False
        )
        row = {
            "epoch": epoch,
            "train_loss": round(tr_loss, 4),
            "train_acc": round(tr_acc, 4),
            "val_loss": round(va_loss, 4),
            "val_acc": round(va_acc, 4),
        }
        history.append(row)
        print(row)
        if va_acc >= best_acc:
            best_acc = va_acc
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "classes": train_ds.classes,
                    "img_size": args.img_size,
                    "val_acc": best_acc,
                    "arch": "mobilenet_v3_small",
                },
                args.out,
            )
            print(f"  guardado {args.out} (val_acc={best_acc:.3f})")

    metrics_path = args.out.with_suffix(".metrics.json")
    metrics_path.write_text(
        json.dumps({"best_val_acc": best_acc, "history": history}, indent=2),
        encoding="utf-8",
    )
    print(f"Listo. Mejor val_acc={best_acc:.3f}")


if __name__ == "__main__":
    main()
