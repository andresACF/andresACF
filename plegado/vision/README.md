# Dobla Visión — clasificador RGB de prendas

Clases v1: `camiseta` | `pantalon` | `toalla` | `otro` | `vacio`

## Arranque rápido

```bash
cd plegado/vision
pip install -r requirements.txt
python3 prepare_seed_dataset.py --per-class 80   # seed sintético (smoke test)
python3 train.py --epochs 8
python3 infer.py --image data/val/camiseta/seed_camiseta_0000.jpg --json
```

El seed **no** es tu ropa. Sirve para validar el pipeline. El modelo útil
sale cuando metes fotos reales del tacho.

## Añadir fotos reales (lo importante)

1. Cámara fija top-down sobre el tacho / mesa.
2. Copia JPG/PNG en:

```
data/train/camiseta/
data/train/pantalon/
data/train/toalla/
data/train/otro/
data/train/vacio/
data/val/...   (mismo esquema, ~20 %)
```

3. Reentrena:

```bash
python3 train.py --epochs 15 --out checkpoints/dobla_garment.pt
```

Meta: ≥200 fotos por clase de **tu** entorno (luz, tacho, ropa).

## Salida de inferencia

```json
{
  "tipo": "camiseta",
  "confianza": 0.91,
  "bbox": [0, 0, 640, 480],
  "grasp": [320, 240]
}
```

`grasp` v1 = centro del frame. Cuando agreguemos detección (YOLO), bbox/grasp
vendrán del objeto.

## Archivos

| Archivo | Rol |
|---------|-----|
| `prepare_seed_dataset.py` | Dataset sintético de prueba |
| `train.py` | Fine-tune MobileNetV3-Small |
| `infer.py` | Predicción JSON |
| `classes.json` | Nombres de clase |
| `checkpoints/dobla_garment.pt` | Pesos entrenados |

Ver también [`../hardware/VISION.md`](../hardware/VISION.md).
