# Lista de materiales (BOM)

Costos aproximados en USD (pueden variar por país/tienda). Pensado para
conseguir piezas en Mercado Libre, Amazon, AliExpress o ferretería local.

## Electrónica

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | ESP32 DevKit (30 pines) | 1 | $6–12 | Con USB-C preferible |
| 2 | Servo MG996R o DS3218 (metal) | 4 | $8–15 c/u | No uses SG90: no tienen torque |
| 3 | Fuente 5 V 10 A (meanwell/genérica) | 1 | $12–25 | Crítico: no alimentar servos desde el USB |
| 4 | Botón pulsador momentáneo 12 mm | 1 | $1 | Doblar |
| 5 | Botón pulsador (reset / emergencia) | 1 | $1 | Opcional, NC a GND |
| 6 | LED 5 mm + resistencia 220 Ω | 1 | $0.50 | Estado “ocupado” |
| 7 | Protoboard o PCB perforada | 1 | $2–5 | |
| 8 | Cable duplex 22–24 AWG | 5 m | $3 | Señal + 5 V / GND |
| 9 | Conectores Dupont / bornes | 1 set | $2 | |
|10 | Capacitor 1000 µF 16 V | 1 | $1 | En paralelo a la alimentación de servos |

**Subtotal electrónica:** ~$60–100

## Mecánica

| # | Pieza | Cant. | Est. | Notas |
|---|-------|------:|-----:|-------|
| 1 | MDF o triplay 6–9 mm | 1 pliego | $8–15 | Base + 3 paneles |
| 2 | Bisagras piano o 8 bisagras chicas | 1 set | $4–8 | Paneles izq/der/abajo |
| 3 | Ejes / bielas de servo (horquilla + varilla M3) | 4 sets | $6–12 | O imprime en 3D |
| 4 | Tornillos M3 + tuercas + arandelas | 1 set | $3 | |
| 5 | Esquinas / soportes en L de metal | 4–6 | $3 | Marco y bascula |
| 6 | Canasta de ropa rígida | 1 | $5–15 | La que ya tengas sirve |
| 7 | Patas antideslizantes / goma | 4 | $2 | |
| 8 | Cinta antideslizante (opcional) | 1 | $3 | Sobre la tabla para que no resbale la ropa |
| 9 | Pintura / barniz sellador | — | $5 | Evita que el MDF se hinche |

**Subtotal mecánica:** ~$40–70

## Herramientas (si no las tienes)

- Destornilladores, taladro, sierra caladora o sierra de mesa
- Soldador + estaño (recomendado para uniones firmes)
- Multímetro
- Impresora 3D (opcional, para brazos de servo)

## Costo total orientativo

| Escenario | Rango |
|-----------|------:|
| Aprovechando canasta y herramientas | **$80–120** |
| Comprando casi todo nuevo | **$120–180** |

## Sustituciones válidas

- **Sin ESP32:** Arduino Uno + módulo USB-serial funciona, pero Web Serial igual.
- **Servos más baratos:** MG995 puede servir para camisetas; con jeans fallará antes.
- **Tabla lista:** un FlipFold comercial + motorizar las bisagras acorta el trabajo de carpintería.

## Lo que NO hace falta (aún)

- Cámara / visión artificial
- Brazo robótico de 6 ejes
- Raspberry Pi (el ESP32 alcanza)
- Impresión 3D obligatoria
