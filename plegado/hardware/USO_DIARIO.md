# Uso diario — sistema automático

## Objetivo (cuando A+B+C estén integrados)

1. Echa la ropa al **tacho de entrada**.
2. Pulsa **Iniciar lote** (o detección automática de carga).
3. Espera: el sistema saca, identifica, extiende, dobla y apila.
4. Retira la **canasta de salida**.

No extiendes prendas. No eliges tipo (salvo override en la UI).

## Mientras solo tengas el módulo C

Sigue el flujo semi:

1. Enciende fuente 5 V + ESP32.
2. Extiende una prenda en la tabla.
3. Botón / web → dobla → canasta.
4. Repite.

Así entrenas hábitos y calibras C antes de automatizar A/B.

## Durante un lote automático

- LED/UI: `idle` | `picking` | `classifying` | `folding` | `done` | `error`
- Si `error` (agarre fallido / prenda `otro`): deja esa prenda en bandeja de
  rechazo o pide ayuda; continúa con la siguiente.
- Parada de emergencia: corta motores B y servos C.

## Qué echar al tacho (v1)

| Sí | No |
|----|----|
| Camisetas, polos | Sábanas ajustadas |
| Toallas medianas | Abrigos / edredones |
| Pantalones finos | Ropa empapada |
| Fundas | Cables, zapatos, objetos duros |

## Mantenimiento

- Semanal: pelusa en tabla y tacho, tornillos de pinza/bielas.
- Revisar enfoque y limpieza del lente de la cámara.
- Recalibrar ángulos del módulo C si aparece roce.

## Checklist “automático listo”

- [ ] Llenas el tacho, pulsas iniciar, no tocas hasta el final
- [ ] ≥7/10 prendas terminan dobladas en la canasta
- [ ] Las fallidas van a rechazo sin atascar la línea
- [ ] Sabes dónde está el kill switch
