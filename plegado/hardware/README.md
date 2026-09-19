# Dobla Hardware

Sistema automático: **tacho → visión → agarre → plegado → canasta**.

Tú echas la ropa al tacho. La máquina separa, identifica (RGB), extiende,
dobla y apila. El plegado con tabla+servos es solo el **módulo C**.

## Empieza aquí

1. **Plano completo:** [`ARQUITECTURA.md`](./ARQUITECTURA.md)
2. **Materiales por módulo:** [`BOM.md`](./BOM.md)
3. **Módulo C (plegado, ya construible):** [`MONTAJE.md`](./MONTAJE.md)
4. **Módulo A (visión RGB):** [`VISION.md`](./VISION.md)
5. **Módulo B (agarre):** [`AGARRE.md`](./AGARRE.md)
6. **Uso diario objetivo:** [`USO_DIARIO.md`](./USO_DIARIO.md)
7. **Firmware C:** [`../firmware/dobla_fold/`](../firmware/dobla_fold/)

## Flujo objetivo

```
tacho de entrada → cámara RGB → pinza saca 1 prenda
      → extiende en tabla → servos pliegan → canasta
```

## Orden de build

| Fase | Qué | ¿Usable solo? |
|------|-----|---------------|
| 0 | Módulo C — tabla motorizada | Sí (colocas a mano) |
| 1 | Módulo A — clasificador RGB | Sí (ayuda + telemetría) |
| 2 | Módulo B — agarre/extender | Junto con A+C = automático |
| 3 | Orquestador de lote | Un botón “vaciar tacho” |

## Seguridad

- Fuentes separadas: 5 V servos C, 12–24 V motores B, lógica a parte.
- Parada de emergencia corta todo.
- No metas la mano en tacho ni tabla en movimiento.
- Fija la canasta de salida.
