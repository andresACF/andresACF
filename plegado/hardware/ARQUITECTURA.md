# Dobla — sistema automático de plegado

**Visión de producto:** echas la ropa sucia/seca a un **tacho**. El sistema
separa una prenda, la identifica, la extiende, la dobla y la deja en la
**canasta**. Tú no colocas nada a mano.

```
  [TACHO de entrada]
         │
         ▼
  ┌──────────────┐
  │  A · Visión  │  cámara RGB (clasifica + localiza agarre)
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  B · Agarre  │  brazo / pinza saca 1 prenda y la extiende
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  C · Plegado │  tabla motorizada (4 servos) → ya documentada
  └──────┬───────┘
         ▼
  [CANASTA de salida]
```

## Experiencia de uso diario (objetivo)

1. Tiras el montón al tacho de entrada.
2. Pulsas **Iniciar** (o arranca solo al detectar carga).
3. Esperas. El sistema procesa prenda por prenda.
4. Retiras la canasta con la ropa doblada.

Sin extender prendas. Sin elegir tipo a mano (salvo override).

## Por qué no RGB-D obligatorio

| Tarea | Sensor recomendado |
|-------|--------------------|
| Identificar tipo (camiseta / pantalón / toalla) | **RGB** basta |
| Localizar un borde/agarre en el montón | RGB + buen ángulo; RGB-D ayuda |
| Estimar grosor / capas / nudos difíciles | RGB-D útil, no v1 |

**Decisión de planos:** v1 de visión = **cámara RGB** top-down sobre el tacho
y/o la mesa. RGB-D queda como mejora opcional del módulo B.

## Módulos

| Módulo | Función | Estado en este repo |
|--------|---------|---------------------|
| **A · Visión** | Detectar prenda, clasificar, proponer punto de agarre | Plan + dataset notes |
| **B · Agarre / extender** | Sacar del tacho y dejar plana en la tabla | Plan mecánico |
| **C · Plegado** | Doblar y volcar a canasta | **Implementado** (firmware + MONTAJE) |

Construimos **C primero** (ya funciona solo), luego A, luego B. Así siempre
tienes algo usable mientras crece la autonomía.

## Fases de construcción

### Fase 0 — Ya listo (módulo C)
Tabla FlipFold + ESP32 + canasta. Uso: colocas una prenda y dobla.
Docs: [`MONTAJE.md`](./MONTAJE.md), [`BOM.md`](./BOM.md) § C.

### Fase 1 — Visión (módulo A)
- Cámara USB/CSI sobre el tacho o la mesa
- PC / Jetson / RPi 5 corre el clasificador
- Salida: `{tipo, bbox, grasp_xy}` por serial/MQTT al controlador
- Dataset: fotos top-down propias (sin RGB-D)

Docs: [`VISION.md`](./VISION.md)

### Fase 2 — Agarre (módulo B)
- Brazo bajo costo (3–4 DoF) o pórtico XY + pinza
- Estrategia v1: pinza de dos dedos + vibración/sacudida para soltar una prenda
- Deja la prenda en la tabla → dispara `FOLD` al ESP32

Docs: [`AGARRE.md`](./AGARRE.md)

### Fase 3 — Integración automática
- Orquestador: `while tacho_no_vacio: pick → classify → place → fold → stack`
- UI: un botón **Iniciar lote**
- Uso diario: [`USO_DIARIO.md`](./USO_DIARIO.md)

## Documentos

| Archivo | Contenido |
|---------|-----------|
| [`ARQUITECTURA.md`](./ARQUITECTURA.md) | Este plano (sistema completo) |
| [`BOM.md`](./BOM.md) | Materiales por módulo A/B/C |
| [`MONTAJE.md`](./MONTAJE.md) | Montaje del módulo C (plegado) |
| [`VISION.md`](./VISION.md) | Clasificador RGB y dataset |
| [`AGARRE.md`](./AGARRE.md) | Brazo / pinza / extender |
| [`USO_DIARIO.md`](./USO_DIARIO.md) | Rutina objetivo + fallbacks |
| [`../firmware/dobla_fold/`](../firmware/dobla_fold/) | Firmware módulo C |

## Coste orientativo (sistema completo DIY)

| Alcance | Rango USD |
|---------|----------:|
| Solo módulo C (hoy) | 80–180 |
| C + visión RGB (Fase 1) | 150–350 |
| C + visión + agarre simple (Fase 2) | 400–900+ |

Industrial comercial existe para toallas/hoteles; para ropa mixta de casa
sigue siendo terreno DIY / startups caras. Este plano es la ruta casera.
