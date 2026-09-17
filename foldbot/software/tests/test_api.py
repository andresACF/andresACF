"""Pruebas de la API local de clasificación."""

import base64
import io

import pytest

from foldbot_ai.api import app
from foldbot_ai.sample_gen import GENERATORS


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c


def _png_bytes(name: str) -> bytes:
    buf = io.BytesIO()
    GENERATORS[name]().save(buf, format="PNG")
    return buf.getvalue()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_classes(client):
    r = client.get("/classes")
    assert r.status_code == 200
    assert "camiseta" in r.get_json()["classes"]


def test_classify_multipart(client):
    data = {"image": (io.BytesIO(_png_bytes("pantalon")), "pantalon.png")}
    r = client.post("/classify", data=data, content_type="multipart/form-data")
    assert r.status_code == 200
    body = r.get_json()
    assert body["tipo"] == "pantalon"
    assert 0.0 <= body["confianza"] <= 1.0
    assert body["agarre"]["z"] is None


def test_classify_base64_json(client):
    b64 = base64.b64encode(_png_bytes("toalla")).decode()
    r = client.post("/classify", json={"image_b64": b64})
    assert r.status_code == 200
    assert r.get_json()["tipo"] == "toalla"


def test_classify_missing_image(client):
    r = client.post("/classify", json={})
    assert r.status_code == 400
    assert "error" in r.get_json()
