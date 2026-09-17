"""API local de clasificación (MVP sin cámara).

Expone el contrato IA -> Orquestador como un endpoint HTTP para poder integrar y
probar sin hardware:

    POST /classify
        - multipart/form-data con campo ``image`` (archivo), o
        - application/json  con ``{"image_b64": "<base64>"}``
      -> 200 {"tipo", "confianza", "agarre": {...}, "scores": {...}, "modelo"}

    GET /health -> {"status": "ok", "modelo": ...}
    GET /classes -> {"classes": [...]}

Ejecutar:
    python -m foldbot_ai.api           # escucha en 0.0.0.0:8000
"""

from __future__ import annotations

import base64
import io
import os

from flask import Flask, jsonify, request
from PIL import Image, UnidentifiedImageError

from .model import CLASSES, load_default_classifier

app = Flask(__name__)
_classifier = load_default_classifier()


def _read_image_from_request() -> Image.Image:
    """Extrae la imagen del request (multipart o JSON base64)."""
    if "image" in request.files:
        return Image.open(request.files["image"].stream)

    if request.is_json:
        data = request.get_json(silent=True) or {}
        b64 = data.get("image_b64")
        if b64:
            raw = base64.b64decode(b64)
            return Image.open(io.BytesIO(raw))

    raise ValueError(
        "Falta la imagen. Envíe multipart 'image' o JSON {'image_b64': ...}."
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "modelo": _classifier.name})


@app.get("/classes")
def classes():
    return jsonify({"classes": CLASSES})


@app.post("/classify")
def classify():
    try:
        image = _read_image_from_request()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "No se pudo decodificar la imagen."}), 400

    result = _classifier.classify(image)
    payload = result.to_dict()
    payload["modelo"] = _classifier.name
    return jsonify(payload)


def main():
    host = os.environ.get("FOLDBOT_HOST", "0.0.0.0")
    port = int(os.environ.get("FOLDBOT_PORT", "8000"))
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
