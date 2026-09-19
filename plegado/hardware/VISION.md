# Módulo A — Visión (RGB)

Objetivo: mirar el tacho (o la mesa) y decir **qué prenda hay** y **dónde
agarrarla**. Sin cámara de profundidad en v1.

## Hardware

| Pieza | Notas |
|-------|-------|
| Cámara USB 1080p (o CSI en RPi) | Fija, top-down, buena luz |
| Iluminación LED difusa | Evita sombras duras |
| RPi 5 / mini-PC / Jetson Nano | Corre inferencia |
| Soporte / brazo gooseneck | Altura estable ~60–80 cm sobre el tacho |

**No hace falta RGB-D** para clasificar tipo. Opcional más adelante para agarres difíciles.

## Salida del modelo

```json
{
  "tipo": "camiseta",
  "confianza": 0.91,
  "bbox": [120, 80, 400, 360],
  "grasp": [260, 200]
}
```

Clases v1: `camiseta` | `pantalon` | `toalla` | `otro` | `vacio`.

## Dataset (entrenar en casa)

1. Monta la cámara fija sobre el tacho / mesa.
2. Tira fotos reales: 1 prenda, 2–3 enredadas, vacía, distinta luz.
3. ~200–500 imágenes por clase ya sirven para un prototipo.
4. Etiqueta tipo (+ bbox si haces detección, no solo clasificación).
5. Augmentación: rotación, brillo, crop.

Herramientas: Roboflow, Label Studio, o carpetas simples si solo clasificas.

## Modelo v1 sugerido

- Clasificación: MobileNet / EfficientNet fine-tune (rápido en RPi).
- Si necesitas bbox/grasp: YOLO nano o similar sobre el mismo dataset.
- Inferencia local; el ESP32 solo recibe órdenes (`FOLD`, etc.).

## Integración

```
cámara → inferencia (RPi) → {tipo, grasp}
                │
                ├─→ módulo B (mueve pinza a grasp)
                └─→ (opcional) UI web muestra tipo detectado
```

Cuando B deje la prenda en la tabla, el orquestador manda `FOLD` al ESP32
(módulo C), igual que hoy por Web Serial / UART.

## Criterio de listo

- [ ] ≥90 % acierto en camiseta/pantalón/toalla con tu ropa real
- [ ] Detecta `vacio` para parar el lote
- [ ] Latencia &lt; 300 ms por frame en tu hardware
- [ ] Funciona con la luz de tu cuarto de lavado (no solo lab)
