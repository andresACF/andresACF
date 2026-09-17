# 05 — Presupuesto y BOM por módulo

> Cifras en **USD**, orden de magnitud para hobby/estudiante. Varían mucho por
> país e importación. Prioridad: `A` = comprar ya, `B` = medio plazo, `C` = al
> final / opcional.

## Resumen por módulo

| Módulo | Rango estimado | Cuándo |
| --- | --- | --- |
| A — Cámara RGB-D | $150 – $350 | Noviembre |
| C — Brazo (servos, estructura, electrónica) | $80 – $200 | Fase 1 |
| Pinza suave / materiales | $15 – $40 | Fase 1 |
| D — Tablero de plegado (paneles, bisagras, 3 servos) | $60 – $150 | Fase 1 |
| Control (Pi/Arduino/fuentes/cables) | $50 – $120 | Fase 1 |
| **Total prototipo v1** | **$355 – $860** | |

## Módulo A — Cámara RGB-D

| Ítem | Cant. | Costo unit. | Subtotal | Prioridad | Notas |
| --- | --- | --- | --- | --- | --- |
| Intel RealSense D435/D435i (preferida) | 1 | $150–$350 | $150–$350 | A (nov) | Buen SDK, comunidad grande |
| *Alt:* Orbbec Astra / Femto Lite | 1 | $100–$200 | — | — | SDK distinto, más barata |
| Soporte cenital impreso (PLA) | 1 | ~$3 | $3 | A | Ver `cad/camera_mount.scad` |

## Módulo C — Brazo DIY

| Ítem | Cant. | Costo unit. | Subtotal | Prioridad |
| --- | --- | --- | --- | --- |
| Servo hombro DS3218 (20 kg·cm) | 1 | $12–$18 | $12–$18 | A |
| Servo MG996R (base/codo/muñeca) | 3 | $4–$7 | $12–$21 | A |
| Servo pinza SG90/MG90S | 1 | $2–$4 | $2–$4 | A |
| Filamento PLA/PETG (eslabones) | ~0.5 kg | $20/kg | ~$10 | A |
| Rodamiento 608ZZ (base) | 2 | $1 | $2 | B |
| Tornillería M3 + insertos | set | ~$8 | $8 | A |
| Varilla/estructura aluminio (opcional) | — | $10–$30 | $10–$30 | C |
| **Subtotal brazo** | | | **~$58–$93** | |

## Pinza suave

| Ítem | Cant. | Costo unit. | Subtotal | Prioridad |
| --- | --- | --- | --- | --- |
| Filamento TPU (dedos flexibles) | ~0.1 kg | $30/kg | ~$3 | A |
| Almohadilla silicona/espuma | 1 | $5–$10 | $5–$10 | A |
| Sensor tacto/FSR (opcional) | 1 | $5–$12 | $5–$12 | C |

## Módulo D — Tablero de plegado

| Ítem | Cant. | Costo unit. | Subtotal | Prioridad |
| --- | --- | --- | --- | --- |
| Panel MDF/acrílico 5 mm (400×450) | 1 | $8–$15 | $8–$15 | A |
| Bisagra de piano (o varilla + PLA) | 1 | $5–$10 | $5–$10 | A |
| Servo solapa MG996R/DS3218 | 3 | $5–$15 | $15–$45 | A |
| Barras de empuje + rótulas | set | $5–$10 | $5–$10 | B |
| Tornillería y soportes impresos | set | ~$8 | $8 | A |
| **Subtotal tablero** | | | **~$41–$96** | |

## Control y alimentación

| Ítem | Cant. | Costo unit. | Subtotal | Prioridad |
| --- | --- | --- | --- | --- |
| ESP32 DevKit | 1 | $6–$10 | $6–$10 | A |
| Raspberry Pi (o usar PC existente) | 0–1 | $35–$60 | $0–$60 | B |
| PCA9685 (driver PWM 16ch) | 1 | $3–$6 | $3–$6 | A |
| Fuente 6V 10–20A (servos) | 1 | $15–$30 | $15–$30 | A |
| Fuente 5V 3A (lógica) | 1 | $6–$10 | $6–$10 | A |
| Condensadores (bulk + cerámicos) | set | ~$5 | $5 | A |
| Fusible + portafusible | 1 | ~$3 | $3 | A |
| Cableado AWG16-18 + Dupont | set | $8–$15 | $8–$15 | A |
| **Subtotal control** | | | **~$46–$139** | |

## Notas de compra

- Empezar por **prioridad A** de brazo, tablero y control (permite avanzar Fase
  1 sin cámara).
- La **cámara** es la compra grande y se deja para noviembre; hasta entonces el
  software (Módulo B) usa fotos del celular / datasets públicos.
- Comprar **1–2 servos de repuesto** del hombro (es el que más sufre).

> Este BOM es una **estimación inicial**. Refinar con precios reales del
> proveedor local antes de comprar y actualizar esta tabla.
