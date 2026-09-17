"""Segmentación simple de la prenda respecto al fondo.

Supone un fondo relativamente uniforme (mesa limpia, ver suposiciones en
``docs/01-arquitectura.md``). Estima el color de fondo a partir de las esquinas y
marca como "prenda" los píxeles suficientemente distintos del fondo.

En Fase 3, con la cámara RGB-D, esta segmentación se reemplaza/mejora usando la
profundidad (el blob más alto es la prenda), pero la interfaz ``Silhouette`` se
mantiene.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from PIL import Image


@dataclass
class Silhouette:
    """Silueta binaria de la prenda y sus métricas geométricas."""

    mask: List[List[bool]]  # [y][x] True = prenda
    image_w: int
    image_h: int
    bbox: Tuple[int, int, int, int]  # (x0, y0, x1, y1) inclusive
    area: int  # nº de píxeles de prenda
    centroid_x: float
    centroid_y: float

    def features(self) -> Dict[str, float]:
        x0, y0, x1, y1 = self.bbox
        bw = max(1, x1 - x0 + 1)
        bh = max(1, y1 - y0 + 1)
        aspect = bh / bw
        fill = self.area / (bw * bh)
        area_frac = self.area / max(1, self.image_w * self.image_h)

        # bottom_gap: fracción del TERCIO CENTRAL de columnas cuya mitad inferior
        # está vacía. Detecta la horqueta de un pantalón (gap central entre
        # piernas) sin confundirse con las mangas de una camiseta (gaps
        # laterales, no centrales).
        mid_y = (y0 + y1) // 2
        cx0 = x0 + bw // 3
        cx1 = x0 + (2 * bw) // 3
        center_cols = max(1, cx1 - cx0 + 1)
        empty_center = 0
        for x in range(cx0, cx1 + 1):
            col_has_bottom = any(self.mask[y][x] for y in range(mid_y, y1 + 1))
            if not col_has_bottom:
                empty_center += 1
        bottom_gap = empty_center / center_cols

        return {
            "aspect": round(aspect, 4),
            "fill": round(fill, 4),
            "area_frac": round(area_frac, 4),
            "bottom_gap": round(bottom_gap, 4),
            "bbox_w": bw,
            "bbox_h": bh,
        }


def _bg_color(px, w: int, h: int) -> Tuple[int, int, int]:
    """Estima el color de fondo promediando las 4 esquinas."""
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    r = g = b = 0
    for (x, y) in corners:
        c = px[x, y]
        r += c[0]
        g += c[1]
        b += c[2]
    n = len(corners)
    return (r // n, g // n, b // n)


def segment_garment(image: Image.Image, threshold: int = 40) -> Silhouette:
    """Segmenta la prenda del fondo y devuelve su ``Silhouette``.

    ``threshold`` es la distancia (Manhattan en RGB) mínima respecto al fondo
    para considerar un píxel como prenda.
    """
    img = image.convert("RGB")
    # Reescalar para acotar el coste (máx. 256 px de lado mayor).
    max_side = 256
    if max(img.size) > max_side:
        scale = max_side / max(img.size)
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))))

    w, h = img.size
    px = img.load()
    bg = _bg_color(px, w, h)

    mask = [[False] * w for _ in range(h)]
    area = 0
    sum_x = 0.0
    sum_y = 0.0
    x0, y0, x1, y1 = w, h, -1, -1

    for y in range(h):
        row = mask[y]
        for x in range(w):
            c = px[x, y]
            dist = abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2])
            if dist >= threshold:
                row[x] = True
                area += 1
                sum_x += x
                sum_y += y
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y

    if area == 0:
        # Sin prenda detectada: silueta vacía centrada.
        return Silhouette(
            mask=mask,
            image_w=w,
            image_h=h,
            bbox=(0, 0, w - 1, h - 1),
            area=0,
            centroid_x=w / 2,
            centroid_y=h / 2,
        )

    return Silhouette(
        mask=mask,
        image_w=w,
        image_h=h,
        bbox=(x0, y0, x1, y1),
        area=area,
        centroid_x=sum_x / area,
        centroid_y=sum_y / area,
    )
