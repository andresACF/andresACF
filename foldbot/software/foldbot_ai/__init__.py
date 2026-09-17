"""Foldbot AI — scaffold de clasificación de prendas y estimación de agarre.

Este paquete es el MVP de software (Fase 2) que se puede desarrollar y probar
*sin* la cámara ni el hardware. Implementa el contrato IA -> Orquestador descrito
en ``docs/01-arquitectura.md``:

    POST /classify  ->  {"tipo", "confianza", "agarre": {"x","y","z"}}

El clasificador por defecto (``HeuristicClassifier``) usa características simples
de la silueta (relación de aspecto, relleno, simetría) para funcionar sin un
modelo entrenado. En Fase 2 se sustituye por ``TorchClassifier`` (transfer
learning con MobileNetV2 / EfficientNet-lite) manteniendo la misma interfaz.
"""

from .model import (
    CLASSES,
    BaseClassifier,
    HeuristicClassifier,
    ClassificationResult,
    load_default_classifier,
)

__all__ = [
    "CLASSES",
    "BaseClassifier",
    "HeuristicClassifier",
    "ClassificationResult",
    "load_default_classifier",
]

__version__ = "0.1.0"
