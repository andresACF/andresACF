"""Genera un dataset seed sintético top-down para probar el pipeline.

NO reemplaza fotos reales de tu tacho. Sirve para:
- Verificar que train.py / infer.py funcionan
- Tener un checkpoint inicial que luego fine-tuneas con tu ropa

Uso:
  python3 prepare_seed_dataset.py --per-class 80
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CLASSES = ["camiseta", "pantalon", "toalla", "otro", "vacio"]


def bg(size: int, rng: random.Random) -> Image.Image:
    """Fondo tipo mesa / tacho (gris cálido con ruido)."""
    base = tuple(rng.randint(170, 210) for _ in range(3))
    img = Image.new("RGB", (size, size), base)
    draw = ImageDraw.Draw(img)
    for _ in range(400):
        x, y = rng.randint(0, size - 1), rng.randint(0, size - 1)
        c = tuple(max(0, min(255, base[i] + rng.randint(-25, 25))) for i in range(3))
        draw.point((x, y), fill=c)
    # borde de tacho
    if rng.random() < 0.7:
        m = rng.randint(8, 28)
        draw.rectangle([m, m, size - m, size - m], outline=(110, 90, 70), width=rng.randint(3, 8))
    return img


def blob(draw: ImageDraw.ImageDraw, box, color, rng: random.Random) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=rng.randint(8, 28), fill=color)
    # pliegues / arrugas
    for _ in range(rng.randint(2, 6)):
        xa = rng.randint(x0, x1)
        ya = rng.randint(y0, y1)
        xb = rng.randint(x0, x1)
        yb = rng.randint(y0, y1)
        shade = tuple(max(0, c - rng.randint(10, 40)) for c in color)
        draw.line([(xa, ya), (xb, yb)], fill=shade, width=rng.randint(1, 3))


def draw_camiseta(img: Image.Image, rng: random.Random) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    color = rng.choice(
        [(40, 90, 180), (30, 140, 120), (200, 60, 60), (240, 240, 240), (40, 40, 40)]
    )
    cx, cy = w // 2 + rng.randint(-20, 20), h // 2 + rng.randint(-20, 20)
    bw, bh = rng.randint(90, 140), rng.randint(100, 150)
    blob(d, [cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2], color, rng)
    # mangas
    sleeve = tuple(max(0, c - 15) for c in color)
    blob(d, [cx - bw // 2 - 40, cy - bh // 3, cx - bw // 2 + 10, cy], sleeve, rng)
    blob(d, [cx + bw // 2 - 10, cy - bh // 3, cx + bw // 2 + 40, cy], sleeve, rng)


def draw_pantalon(img: Image.Image, rng: random.Random) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    color = rng.choice(
        [(30, 50, 90), (50, 50, 50), (70, 90, 120), (100, 70, 40)]
    )
    cx, cy = w // 2 + rng.randint(-15, 15), h // 2 + rng.randint(-15, 15)
    # cintura
    blob(d, [cx - 55, cy - 70, cx + 55, cy - 20], color, rng)
    # piernas
    blob(d, [cx - 55, cy - 25, cx - 5, cy + 80], color, rng)
    blob(d, [cx + 5, cy - 25, cx + 55, cy + 80], color, rng)


def draw_toalla(img: Image.Image, rng: random.Random) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    color = rng.choice(
        [(220, 120, 80), (180, 200, 220), (120, 160, 100), (240, 200, 160)]
    )
    cx, cy = w // 2 + rng.randint(-25, 25), h // 2 + rng.randint(-25, 25)
    bw, bh = rng.randint(120, 180), rng.randint(70, 110)
    if rng.random() < 0.5:
        bw, bh = bh, bw
    blob(d, [cx - bw // 2, cy - bh // 2, cx + bw // 2, cy + bh // 2], color, rng)
    # franjas
    for i in range(3):
        y = cy - bh // 2 + (i + 1) * bh // 4
        d.line([(cx - bw // 2 + 8, y), (cx + bw // 2 - 8, y)], fill=(255, 255, 255), width=2)


def draw_otro(img: Image.Image, rng: random.Random) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    color = rng.choice([(160, 40, 160), (200, 180, 40), (20, 20, 20)])
    # forma irregular / calcetines / cable-ish
    for _ in range(rng.randint(2, 5)):
        x0 = rng.randint(40, w - 80)
        y0 = rng.randint(40, h - 80)
        blob(d, [x0, y0, x0 + rng.randint(30, 70), y0 + rng.randint(20, 50)], color, rng)


def make_image(label: str, size: int, rng: random.Random) -> Image.Image:
    img = bg(size, rng)
    if label == "camiseta":
        draw_camiseta(img, rng)
    elif label == "pantalon":
        draw_pantalon(img, rng)
    elif label == "toalla":
        draw_toalla(img, rng)
    elif label == "otro":
        draw_otro(img, rng)
    # vacio: solo fondo
    if rng.random() < 0.4:
        img = img.filter(ImageFilter.GaussianBlur(radius=rng.uniform(0.2, 1.2)))
    return img


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-class", type=int, default=80)
    parser.add_argument("--size", type=int, default=224)
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    counts = {"train": {}, "val": {}}

    for split in ("train", "val"):
        for c in CLASSES:
            (DATA / split / c).mkdir(parents=True, exist_ok=True)
            counts[split][c] = 0

    for c in CLASSES:
        n_val = max(1, int(args.per_class * args.val_ratio))
        n_train = args.per_class - n_val
        for i in range(n_train):
            img = make_image(c, args.size, rng)
            path = DATA / "train" / c / f"seed_{c}_{i:04d}.jpg"
            img.save(path, quality=90)
            counts["train"][c] += 1
        for i in range(n_val):
            img = make_image(c, args.size, rng)
            path = DATA / "val" / c / f"seed_{c}_{i:04d}.jpg"
            img.save(path, quality=90)
            counts["val"][c] += 1

    meta = {
        "source": "synthetic_seed",
        "warning": "Fine-tune with real top-down photos from your laundry bin.",
        "classes": CLASSES,
        "counts": counts,
    }
    (DATA / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))
    print(f"Dataset listo en {DATA}")


if __name__ == "__main__":
    main()
