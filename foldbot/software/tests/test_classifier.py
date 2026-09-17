"""Pruebas del clasificador heurístico sobre las siluetas de referencia."""

import os

import pytest

from foldbot_ai.model import CLASSES, load_default_classifier
from foldbot_ai.sample_gen import GENERATORS


@pytest.fixture(scope="module")
def clf():
    return load_default_classifier()


@pytest.mark.parametrize("expected", list(GENERATORS.keys()))
def test_silhouettes_classified_correctly(clf, expected):
    """Cada silueta sintética debe clasificarse en su clase."""
    img = GENERATORS[expected]()
    result = clf.classify(img)
    assert result.tipo == expected, (
        f"esperado {expected}, obtenido {result.tipo} (scores={result.scores})"
    )
    assert 0.0 <= result.confianza <= 1.0


def test_result_contract(clf):
    """El resultado cumple el contrato IA -> Orquestador."""
    img = GENERATORS["camiseta"]()
    d = clf.classify(img).to_dict()
    assert set(["tipo", "confianza", "agarre", "scores"]).issubset(d.keys())
    assert d["tipo"] in CLASSES
    assert set(["x", "y", "z"]).issubset(d["agarre"].keys())
    # sin cámara, z es desconocido
    assert d["agarre"]["z"] is None


def test_scores_sum_to_one(clf):
    img = GENERATORS["toalla"]()
    scores = clf.classify(img).scores
    assert set(scores.keys()) == set(CLASSES)
    assert abs(sum(scores.values()) - 1.0) < 1e-6


def test_grasp_centroid_inside_image(clf):
    img = GENERATORS["pantalon"]()
    res = clf.classify(img)
    # centroide normalizado dentro de la imagen [0,1]
    assert 0.0 <= res.agarre["x_norm"] <= 1.0
    assert 0.0 <= res.agarre["y_norm"] <= 1.0
