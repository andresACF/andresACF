#!/usr/bin/env python3
"""Edit the original Canva CV PDF: keep design, update experience."""

from pathlib import Path

import pymupdf as fitz

SRC = Path(__file__).resolve().parent / "assets" / "original_canva.pdf"
OUT = Path(__file__).resolve().parent / "CV_ANDRES_ALFREDO_CORNEJO_FIGUEROA.pdf"
FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

INK = (0x3A / 255, 0x38 / 255, 0x34 / 255)
BEIGE = (0xDF / 255, 0xDA / 255, 0xD4 / 255)
BEIGE_DARK = (0xC0 / 255, 0xB5 / 255, 0xA7 / 255)
WHITE = (1, 1, 1)

JOBS = [
    {
        "date": "Septiembre 2026 - Ahora",
        "company": "SOYODA",
        "meta": "Programador de Sistemas",
        "bullets": [
            "Desarrollo y mantenimiento de sistemas de software.",
            "Soporte y evolución de aplicaciones internas.",
        ],
    },
    {
        "date": "Enero 2026 - Agosto 2026",
        "company": "RIPIO",
        "meta": None,
        "bullets": [
            "Fullstack developer (.NET+ Django +PostgreSQL)",
            "N8N + Desarrollo de agentes de IA",
            "Web Scraping",
            "RPA",
            "LangGraph + Redis + OpenViking(Agent memory)",
            "Docker + Caddy",
            "Celery",
        ],
    },
    {
        "date": "Mayo 2025 - Nov 2025",
        "company": "Banco Guayaquil",
        "meta": "(593) 97 913-0413",
        "bullets": [
            "Manejo del portal Azure (Asignación de Roles en",
            "base a una matriz RBAC, gestión de grupos de",
            "administración)",
            "Active Directory, Trend Vision One y Mosyle.",
            "Power Platform (Power Automate, Power Virtual",
            "Agents)",
            "Reducción del 40% en tiempo de asignación de",
            "licencias de Teams y Microsoft 365 mediante flujos",
            "de Power Automate",
        ],
    },
    {
        "date": "Junio 2025 - Ahora",
        "company": "Consultor Independiente / Desarrollador Fullstack",
        "meta": "(593) 98 359-2954",
        "bullets": [
            "MMN (Sistema de Control de Reparaciones)",
            "PRICOTERCORP(Ecommerce) Contifico + Datafast",
        ],
    },
    {
        "date": "Mayo 2024 - Feb 2025",
        "company": "ESPOL",
        "meta": "+593 98 519 4690",
        "bullets": [
            "Desarrollador Backend y Frontend React + Flutter",
            "Mantenimiento de hardware",
            "API REST",
        ],
    },
]


def main() -> None:
    if not SRC.exists():
        raise SystemExit(
            f"Original Canva PDF not found at {SRC}. "
            "Place the exported PDF there or update SRC."
        )

    doc = fitz.open(SRC)
    page = doc[0]

    # Remove original experience content; keep EXPERIENCIA title and rest of design.
    page.add_redact_annot(fitz.Rect(248, 272, 595.5, 842), fill=WHITE)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    font_reg = str(FONT_DIR / "Poppins-Regular.ttf")
    font_bold = str(FONT_DIR / "Poppins-Bold.ttf")
    font_light = str(FONT_DIR / "Poppins-Light.ttf")

    x0 = 265.0
    line_x = 265.5
    y = 282.0
    bottom = 828.0
    jobs_start_y = y

    for job in JOBS:
        node = fitz.Rect(line_x - 5, y + 1, line_x + 5, y + 11)
        page.draw_rect(node, color=BEIGE_DARK, width=1.2, fill=WHITE, overlay=True)

        date_w = max(110, 10 + len(job["date"]) * 5.0)
        date_rect = fitz.Rect(x0 + 8, y - 1, x0 + 8 + date_w, y + 13)
        page.draw_rect(date_rect, color=BEIGE, fill=BEIGE, overlay=True)
        page.insert_text(
            (x0 + 12, y + 10),
            job["date"],
            fontfile=font_reg,
            fontsize=9.0,
            color=INK,
            overlay=True,
        )
        y += 14.5

        page.insert_text(
            (x0 + 12, y + 9),
            job["company"],
            fontfile=font_bold,
            fontsize=9.0,
            color=INK,
            overlay=True,
        )
        y += 12.5

        if job["meta"]:
            page.insert_text(
                (x0 + 12, y + 9),
                job["meta"],
                fontfile=font_reg,
                fontsize=8.8,
                color=INK,
                overlay=True,
            )
            y += 12

        for bullet in job["bullets"]:
            if y + 11 > bottom:
                break
            page.draw_circle(
                (x0 + 15, y + 4.5), 1.3, color=INK, fill=INK, overlay=True
            )
            page.insert_text(
                (x0 + 21, y + 8),
                bullet,
                fontfile=font_light,
                fontsize=9.0,
                color=INK,
                overlay=True,
            )
            y += 11.8
        y += 4.5

    page.draw_line(
        (line_x, jobs_start_y + 5),
        (line_x, y - 3),
        color=BEIGE_DARK,
        width=1.0,
        overlay=True,
    )

    doc.save(OUT, garbage=4, deflate=True)
    doc.close()
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
