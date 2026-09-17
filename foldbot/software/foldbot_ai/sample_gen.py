"""Genera imágenes de prueba (siluetas sintéticas) de las 4 clases.

No sustituyen a un dataset real; sirven para probar el pipeline end-to-end
(segmentación -> clasificación -> agarre) sin fotos ni cámara.

Uso:
    python -m foldbot_ai.sample_gen                 # escribe en sample_images/
    python -m foldbot_ai.sample_gen --out /tmp/x
"""

from __future__ import annotations

import argparse
import os

from PIL import Image, ImageDraw

BG = (225, 225, 228)
FG = (35, 40, 70)
SIZE = (400, 400)


def _canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", SIZE, BG)
    return img, ImageDraw.Draw(img)


def make_camiseta() -> Image.Image:
    img, d = _canvas()
    # cuerpo central (alto y estrecho)
    d.rectangle([160, 110, 240, 330], fill=FG)
    # mangas cortas arriba (gaps quedan en los LADOS, no en el centro)
    d.rectangle([110, 110, 160, 150], fill=FG)
    d.rectangle([240, 110, 290, 150], fill=FG)
    return img


def make_pantalon() -> Image.Image:
    img, d = _canvas()
    # cintura
    d.rectangle([150, 80, 250, 120], fill=FG)
    # dos piernas con hueco central (horqueta)
    d.rectangle([150, 120, 190, 340], fill=FG)
    d.rectangle([210, 120, 250, 340], fill=FG)
    return img


def make_boxer() -> Image.Image:
    img, d = _canvas()
    # prenda pequeña y ancha
    d.rectangle([120, 175, 280, 250], fill=FG)
    return img


def make_toalla() -> Image.Image:
    img, d = _canvas()
    # rectángulo grande y muy lleno
    d.rectangle([80, 50, 320, 360], fill=FG)
    return img


GENERATORS = {
    "camiseta": make_camiseta,
    "pantalon": make_pantalon,
    "boxer_ropa_interior": make_boxer,
    "toalla": make_toalla,
}


def generate_all(out_dir: str) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for name, fn in GENERATORS.items():
        p = os.path.join(out_dir, f"{name}.png")
        fn().save(p)
        paths.append(p)
    return paths


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Genera siluetas de prueba")
    default_out = os.path.join(os.path.dirname(__file__), "..", "sample_images")
    parser.add_argument("--out", default=os.path.normpath(default_out))
    args = parser.parse_args(argv)
    paths = generate_all(args.out)
    for p in paths:
        print("escrito:", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
