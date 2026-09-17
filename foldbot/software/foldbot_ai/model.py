"""Modelos de clasificación de prendas para Foldbot.

Define:
- ``CLASSES``: las 4 clases objetivo del MVP.
- ``BaseClassifier``: interfaz común (para poder cambiar heurística <-> red neuronal).
- ``HeuristicClassifier``: clasificador sin entrenamiento basado en la silueta.
- ``TorchClassifier``: *stub* documentado para transfer learning (Fase 2).

La estimación del punto de agarre (centroide de la silueta) es común a todos y
vive en ``segmentation.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from PIL import Image

from .segmentation import Silhouette, segment_garment

# Clases objetivo del MVP (ver docs/01-arquitectura.md)
CLASSES: List[str] = ["camiseta", "pantalon", "boxer_ropa_interior", "toalla"]


@dataclass
class ClassificationResult:
    """Resultado que implementa el contrato IA -> Orquestador."""

    tipo: str
    confianza: float
    agarre: Dict[str, Optional[float]]
    scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "confianza": round(self.confianza, 4),
            "agarre": self.agarre,
            "scores": {k: round(v, 4) for k, v in self.scores.items()},
        }


class BaseClassifier:
    """Interfaz común de clasificadores."""

    name: str = "base"

    def classify(self, image: Image.Image) -> ClassificationResult:  # pragma: no cover
        raise NotImplementedError


def _grasp_from_silhouette(sil: Silhouette) -> Dict[str, Optional[float]]:
    """Punto de agarre = centroide de la silueta en px de imagen.

    Sin cámara RGB-D, ``z`` es None (se completará con la profundidad en Fase 3,
    usando el blob más alto). ``x``/``y`` se dan también normalizados [0,1].
    """
    return {
        "x": sil.centroid_x,
        "y": sil.centroid_y,
        "z": None,
        "x_norm": round(sil.centroid_x / sil.image_w, 4) if sil.image_w else None,
        "y_norm": round(sil.centroid_y / sil.image_h, 4) if sil.image_h else None,
    }


def _softmax(scores: Dict[str, float]) -> Dict[str, float]:
    import math

    mx = max(scores.values()) if scores else 0.0
    exps = {k: math.exp(v - mx) for k, v in scores.items()}
    total = sum(exps.values()) or 1.0
    return {k: v / total for k, v in exps.items()}


class HeuristicClassifier(BaseClassifier):
    """Clasificador sin entrenamiento basado en la geometría de la silueta.

    No pretende ser preciso con fotos reales; su función es dar un pipeline
    *funcional* end-to-end (imagen -> etiqueta + agarre) para desarrollar el
    resto del sistema mientras se prepara el dataset y el modelo entrenado.

    Características usadas (todas invariantes a escala):
    - ``aspect``  = alto / ancho del bounding box.
    - ``fill``    = área de la silueta / área del bounding box.
    - ``bottom_gap`` = fracción de columnas del bbox cuya mitad inferior está
      vacía (detecta la "horqueta" entre piernas de un pantalón).
    - ``area_frac`` = área de la silueta / área de la imagen (tamaño relativo).
    """

    name = "heuristic-v1"

    def classify(self, image: Image.Image) -> ClassificationResult:
        sil = segment_garment(image)
        f = sil.features()

        scores: Dict[str, float] = {c: 0.0 for c in CLASSES}

        aspect = f["aspect"]
        fill = f["fill"]
        bottom_gap = f["bottom_gap"]
        area_frac = f["area_frac"]

        # toalla: rectángulo muy lleno (blocky), aspecto moderado, area grande.
        scores["toalla"] += 3.0 * fill
        scores["toalla"] += 1.5 * area_frac
        scores["toalla"] -= 2.0 * bottom_gap
        scores["toalla"] -= 1.0 * abs(aspect - 1.3)

        # pantalon: alto (aspect alto) y con horqueta inferior (bottom_gap alto).
        scores["pantalon"] += 2.5 * max(0.0, aspect - 1.4)
        scores["pantalon"] += 4.0 * bottom_gap
        scores["pantalon"] -= 1.5 * max(0.0, fill - 0.7)

        # camiseta: forma de T -> relleno medio, aspecto ~1, poca horqueta.
        scores["camiseta"] += 2.0 * (1.0 - abs(aspect - 1.05))
        scores["camiseta"] += 2.0 * (1.0 - abs(fill - 0.6))
        scores["camiseta"] -= 2.0 * bottom_gap

        # boxer/ropa interior: prenda pequeña y ancha (aspect < 1), area chica.
        scores["boxer_ropa_interior"] += 2.5 * max(0.0, 1.0 - aspect)
        scores["boxer_ropa_interior"] += 2.5 * max(0.0, 0.35 - area_frac) / 0.35
        scores["boxer_ropa_interior"] += 1.0 * bottom_gap

        probs = _softmax(scores)
        best = max(probs, key=probs.get)
        return ClassificationResult(
            tipo=best,
            confianza=probs[best],
            agarre=_grasp_from_silhouette(sil),
            scores=probs,
        )


class TorchClassifier(BaseClassifier):
    """Stub de clasificador por transfer learning (Fase 2).

    Uso previsto (cuando exista dataset y pesos entrenados)::

        clf = TorchClassifier("weights/foldbot_mobilenet_v2.pt")
        result = clf.classify(img)

    La implementación real cargará MobileNetV2 / EfficientNet-lite, aplicará la
    transformación de entrada estándar y devolverá el mismo ``ClassificationResult``
    (misma interfaz que ``HeuristicClassifier``), de modo que el resto del
    sistema no cambia.
    """

    name = "torch-mobilenetv2"

    def __init__(self, weights_path: str):
        self.weights_path = weights_path

    def classify(self, image: Image.Image) -> ClassificationResult:  # pragma: no cover
        raise NotImplementedError(
            "TorchClassifier es un stub. Entrena un modelo en Fase 2 y carga los "
            "pesos aquí. Mientras tanto usa HeuristicClassifier."
        )


def load_default_classifier() -> BaseClassifier:
    """Devuelve el clasificador por defecto para el MVP (heurístico)."""
    return HeuristicClassifier()
