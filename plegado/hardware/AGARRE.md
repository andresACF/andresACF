# Módulo B — Agarre y extender

Objetivo: sacar **una** prenda del tacho y dejarla **lo bastante plana** en
la tabla del módulo C para que el plegado funcione.

Este es el módulo más difícil. La v1 debe ser tosca pero útil, no un brazo
industrial.

## Enfoque v1 (realista)

1. Cámara da `grasp_xy` (módulo A).
2. Pinza baja, cierra, sube (suele levantar un borde o un puñado).
3. Sacude / golpea suave contra un borde para soltar prendas extra.
4. Lleva la prenda sobre la tabla y abre la pinza (cae más o menos abierta).
5. Opcional: un rodillo o segundo agarre tira de una esquina para extender.
6. Orquestador llama `FOLD` al ESP32.

Si la prenda queda mal extendida, v1 puede: reintentar, o pedir ayuda
(humano coloca esa prenda) y seguir con la siguiente.

## Mecánica sugerida

| Opción | Pros | Contras |
|--------|------|---------|
| **Pórtico XY + eje Z + pinza** | Más barato y repetible | Menos flexible |
| Brazo 4–5 DoF kit | Más “robot” | Calibración dura |
| Cinta + rastrillo / peines | Simple para toallas | Mal con camisetas |

**Recomendación DIY:** pórtico XY de perfil aluminio + servo/stepper Z +
pinza de dos dedos (servo) o vacuum cup suave para telas.

## Electrónica extra (además del ESP32 de plegado)

| Pieza | Rol |
|-------|-----|
| Controlador steppers (CNC shield / drivers TMC) | Ejes XY(Z) |
| Raspberry / PC | Orquesta visión + movimiento |
| Fin de carrera / homing | Calibración |
| Fuente 12–24 V aparte | Motores (nunca del 5 V de servos C) |

Comunicación: RPi manda trayectorias; al terminar el place, UART/`FOLD` al
ESP32 del módulo C.

## Extender la prenda

Sin esto el plegado falla mucho. Ideas en orden de dificultad:

1. **Caída desde altura baja** + mesa antideslizante (mínimo viable).
2. **Segundo punto de agarre**: pinza A sujeta, pinza B tira.
3. **Soplado / cepillo** para abrir mangas (frágil, opcional).

## Criterio de listo

- [ ] Saca 1 prenda del tacho en ≥7/10 intentos
- [ ] La deja en la tabla sin caer al piso
- [ ] Tras place, módulo C completa `FOLD` sin atasco mecánico
- [ ] Parada de emergencia corta motores B y servos C
