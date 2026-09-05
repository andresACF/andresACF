# Firmware Dobla (ESP32)

## Dependencia

En Arduino IDE: biblioteca **ESP32Servo** (Kevin Harrington / madhephaestus).

```
Croquis → Incluir biblioteca → Administrar bibliotecas → "ESP32Servo"
```

El firmware incluye `#include <ESP32Servo.h>`.

## Subir

1. Placa: **ESP32 Dev Module**
2. Puerto: el que aparezca al conectar el USB
3. Velocidad de subida: 921600 (o 115200 si falla)
4. Monitor serial: **115200 baud**

## Protocolo serial

| PC → ESP32 | ESP32 → PC |
|------------|------------|
| `FOLD` | `FOLD_START` … `FOLD_DONE` |
| `HOME` | `HOME_DONE` |
| `STATUS` | `STATUS busy=…` |
| `HELP` | texto de ayuda |
| (al arrancar) | `DOBLA_READY` |

## Prueba sin mecánica

Puedes subir el código con los servos solo enchufados (sin bielas) y ver
que los brazos se mueven al enviar `FOLD`. Calibra ángulos antes de fijar
las varillas a los paneles.

## Perfiles futuros

Hoy el ciclo es único. Si más adelante quieres perfiles por prenda,
añade comandos `FOLD:TEE`, `FOLD:TOWEL` con distintos ángulos/tiempos.
