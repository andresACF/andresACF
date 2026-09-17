# Foldbot — software (scaffold Fase 2)

MVP de software que se desarrolla y prueba **sin cámara ni hardware**. Implementa
el contrato IA → Orquestador de [`../docs/01-arquitectura.md`](../docs/01-arquitectura.md):

```
POST /classify  ->  { "tipo", "confianza", "agarre": {x, y, z}, "scores", "modelo" }
```

## Estructura

```
software/
├── foldbot_ai/
│   ├── model.py          # interfaz + HeuristicClassifier + stub TorchClassifier
│   ├── segmentation.py   # silueta de la prenda (fondo uniforme) + features
│   ├── api.py            # Flask: POST /classify, GET /health, /classes
│   ├── cli.py            # clasifica imágenes locales
│   └── sample_gen.py     # genera siluetas sintéticas de prueba
├── sample_images/        # 4 siluetas de ejemplo (una por clase)
├── tests/                # pytest (clasificador + API)
└── requirements.txt
```

## Instalación

```bash
cd foldbot/software
python -m pip install -r requirements.txt
```

## Uso

### API local

```bash
python -m foldbot_ai.api          # escucha en 0.0.0.0:8000

# en otra terminal:
curl -F "image=@sample_images/camiseta.png" http://localhost:8000/classify
```

Respuesta de ejemplo:

```json
{
  "tipo": "camiseta",
  "confianza": 0.7589,
  "agarre": { "x": 128.0, "y": 129.8, "z": null, "x_norm": 0.5, "y_norm": 0.507 },
  "scores": { "camiseta": 0.7589, "toalla": 0.1267, "boxer_ropa_interior": 0.0934, "pantalon": 0.021 },
  "modelo": "heuristic-v1"
}
```

> `z` es `null` porque sin cámara RGB-D no hay profundidad. En Fase 3 se rellena
> con la altura del blob más alto (punto de agarre real).

### CLI

```bash
python -m foldbot_ai.cli sample_images/*.png
python -m foldbot_ai.cli foto.jpg --json
```

### Regenerar imágenes de prueba

```bash
python -m foldbot_ai.sample_gen
```

## Pruebas

```bash
python -m pytest -v
```

## Del scaffold al modelo real (Fase 2)

El `HeuristicClassifier` **no** usa aprendizaje: clasifica por la geometría de la
silueta (aspecto, relleno, horqueta central, tamaño). Sirve para tener el
pipeline funcionando ya. Para el modelo real:

1. **Dataset:** fotos propias + datasets públicos (DeepFashion / Clothes)
   reetiquetados a las 4 clases: `camiseta`, `pantalon`, `boxer_ropa_interior`,
   `toalla`.
2. **Modelo:** transfer learning (MobileNetV2 / EfficientNet-lite) en PyTorch.
3. **Integración:** implementar `TorchClassifier.classify()` (ya existe el stub en
   `model.py`) devolviendo el mismo `ClassificationResult`. El resto del sistema
   (API, CLI, orquestador) **no cambia**.

## Limitaciones conocidas (MVP)

- La segmentación asume **fondo uniforme y contrastante** (mesa limpia).
- El clasificador heurístico está pensado para **siluetas claras**, no para fotos
  reales complejas: es un andamio para desarrollar el resto, no el modelo final.
