# Lista de materiales (BOM) — por módulos

Costos aproximados en USD. Compra por fases: primero **C**, luego **A**, luego **B**.

---

## Módulo C — Plegado (obligatorio primero)

### Electrónica

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | ESP32 DevKit | 1 | $6–12 | USB-C preferible |
| 2 | Servo MG996R / DS3218 (metal) | 4 | $8–15 c/u | No SG90 |
| 3 | Fuente 5 V 10 A | 1 | $12–25 | Nunca alimentar servos desde USB |
| 4 | Botón Doblar | 1 | $1 | |
| 5 | LED + 220 Ω | 1 | $0.50 | Busy |
| 6 | Protoboard / PCB | 1 | $2–5 | |
| 7 | Cable + Dupont | — | $5 | |
| 8 | Capacitor 1000 µF 16 V | 1 | $1 | En rail 5 V servos |

### Mecánica

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | MDF 6–9 mm | 1 | $8–15 | Tabla + paneles |
| 2 | Bisagras | 1 set | $4–8 | |
| 3 | Bielas M3 / horquillas | 4 | $6–12 | |
| 4 | Tornillería M3 + escuadras | 1 set | $6 | |
| 5 | Canasta de **salida** | 1 | $5–15 | |
| 6 | Antideslizante + barniz | — | $8 | |

**Subtotal C:** ~$80–180

Detalle de montaje: [`MONTAJE.md`](./MONTAJE.md)

---

## Módulo A — Visión RGB

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | Cámara USB 1080p o CSI | 1 | $15–40 | Fija top-down |
| 2 | Raspberry Pi 5 (o PC viejo) | 1 | $0–80 | Inferencia |
| 3 | LED panel / tira difusa | 1 | $8–20 | Luz estable |
| 4 | Soporte cámara | 1 | $5–15 | |
| 5 | MicroSD / disco | 1 | $10 | |

**Subtotal A:** ~$40–170 (menos si ya tienes PC/RPi)

**No incluyas RGB-D en v1.** Plan: [`VISION.md`](./VISION.md)

---

## Módulo B — Agarre / extender

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | Perfil aluminio + ruedas (pórtico XY) | 1 kit | $80–200 | O brazo kit |
| 2 | Steppers NEMA17 + drivers | 2–3 | $40–80 | |
| 3 | Eje Z + pinza (servo o vacuum) | 1 | $25–80 | |
| 4 | Fuente 12–24 V (motores) | 1 | $20–40 | Separada del 5 V |
| 5 | Fines de carrera | 3–6 | $5 | Homing |
| 6 | **Tacho de entrada** rígido | 1 | $10–25 | Boca ancha |
| 7 | Controladora (CNC shield / MCU) | 1 | $15–40 | |

**Subtotal B:** ~$200–500+

Plan: [`AGARRE.md`](./AGARRE.md)

---

## Totales orientativos

| Alcance | Rango |
|---------|------:|
| Solo C (semi, colocas a mano) | $80–180 |
| C + A | $150–350 |
| **Automático C+A+B** | **$400–900+** |

## Sustituciones

- Sin RPi: un laptop viejo corre visión igual.
- Sin pórtico: un brazo educativo barato sirve para prototipo (menos fiable).
- Canasta de entrada = el tacho; canasta de salida = la del módulo C.
