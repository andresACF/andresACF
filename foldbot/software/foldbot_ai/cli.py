"""CLI de prueba: clasifica una imagen local.

Uso:
    python -m foldbot_ai.cli ruta/a/foto.png
    python -m foldbot_ai.cli sample_images/*.png
"""

from __future__ import annotations

import argparse
import json
import sys

from PIL import Image

from .model import load_default_classifier


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Clasificador de prendas Foldbot")
    parser.add_argument("images", nargs="+", help="Rutas de imágenes a clasificar")
    parser.add_argument(
        "--json", action="store_true", help="Salida en JSON (por defecto tabla)"
    )
    args = parser.parse_args(argv)

    clf = load_default_classifier()
    results = []
    for path in args.images:
        try:
            img = Image.open(path)
        except OSError as e:
            print(f"ERROR: no se pudo abrir {path}: {e}", file=sys.stderr)
            return 2
        res = clf.classify(img)
        results.append((path, res))

    if args.json:
        print(json.dumps(
            [{"archivo": p, **r.to_dict()} for p, r in results],
            ensure_ascii=False, indent=2,
        ))
    else:
        print(f"{'archivo':<40} {'tipo':<22} {'conf':>6}  agarre(x,y)")
        print("-" * 80)
        for p, r in results:
            gx = r.agarre.get("x")
            gy = r.agarre.get("y")
            print(f"{p:<40} {r.tipo:<22} {r.confianza:>6.2f}  ({gx:.0f},{gy:.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
