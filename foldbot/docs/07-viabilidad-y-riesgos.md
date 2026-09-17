# 07 — Viabilidad, riesgos y decisiones de calidad

> Este documento es una **auditoría honesta** del diseño. El objetivo del
> proyecto es **calidad/fiabilidad**, no sólo "que se mueva". Aquí se listan los
> puntos débiles reales y las alternativas recomendadas.

## Respuesta directa: ¿el brazo de servos agarrará bien una toalla?

**Con honestidad: el brazo articulado de servos + pinza de dos dedos, tal como
estaba especificado, es la parte más arriesgada y NO es la opción de mayor
calidad.** Funcionará para prendas ligeras y planas en el mejor de los casos,
pero para una **toalla** (sobre todo de baño) tiene dos problemas serios:

1. **El peso puede superar lo asumido.**
2. **Agarrar tela deformable con una pinza es intrínsecamente poco fiable.**

Ambos se detallan abajo, con la recomendación de rediseño.

## Problema 1 — Peso real de las toallas

El supuesto original (200–500 g) se queda corto para toallas grandes:

| Prenda | Peso típico (seco) |
| --- | --- |
| Boxer / ropa interior | 40–120 g |
| Camiseta algodón | 120–220 g |
| **Toalla de manos** | **100–250 g** |
| **Toalla de baño mediana** | **400–700 g** |
| **Toalla de baño grande/afelpada** | **700–1000 g** |

Conclusión: una toalla de baño grande puede **duplicar** la carga útil asumida.

### Impacto en el par del hombro (números)

Recordando el cálculo de [`02-mecanica-brazo.md`](02-mecanica-brazo.md), con el
brazo extendido a `R = 0.36 m`:

```
tau = m · g · R
```

| Carga en la punta | Par sólo por la carga | ¿DS3218 (20 kg·cm ≈ 1.96 N·m)? |
| --- | --- | --- |
| 0.25 kg (toalla manos) | 0.88 N·m ≈ 9 kg·cm | Alcanza, con margen |
| 0.50 kg (asumido) | 1.77 N·m ≈ 18 kg·cm | **Justo al límite** |
| 0.70 kg (toalla baño) | 2.47 N·m ≈ 25 kg·cm | **Insuficiente** |
| 1.00 kg (toalla grande) | 3.53 N·m ≈ 36 kg·cm | **Muy insuficiente** |

Y esto es **sólo la carga**: falta sumar el **peso propio de los eslabones**, que
en un brazo de PLA con servos añade fácilmente otros 10–20 kg·cm en el hombro. Es
decir, con una toalla de baño el hombro con un solo DS3218 **se queda sin par al
extenderse**, sagea y pierde precisión.

Además, los servos hobby (MG996R/DS3218) tienen **backlash/holgura** de ~±1–2°,
que a 0.36 m de alcance son **±6–12 mm** de error de posición y **temblor** bajo
carga: mala repetibilidad justo cuando más importa.

## Problema 2 — Agarrar tela es lo difícil (no el peso)

Aunque el par sobrara, **agarrar ropa desde arriba con una pinza de dos dedos es
un problema abierto y notoriamente poco fiable**:

- Una toalla plana sobre la mesa **no tiene "asa"**: una pinza en el centro sólo
  pellizca aire o resbala. Sólo agarra bien por un **borde/esquina**, y aun así
  levanta la prenda colgando por un punto (no controlada).
- La tela es **deformable**: la forma cambia al tocarla; el punto de agarre "se
  mueve".
- La succión (ventosa) funciona mal en toalla de **rizo poroso** (no sella).

Los robots que doblan ropa de verdad suelen usar **dos brazos + reagarre por los
bordes** o **efectores especializados**. Para un MVP de un solo brazo, hay que
**elegir el efector correcto**, no una pinza genérica.

## Recomendaciones de calidad (rediseño sugerido)

### A) Cambiar el efector: pinza de aguja (needle gripper) para toallas

La forma estándar en la industria de manipular telas "flácidas" es el
**needle/pinch-needle gripper**: agujas finas que entran 1–2 mm en ángulos
opuestos y **enganchan las fibras**. Para **toalla de rizo es idealísimo** y es
DIY-able (un solenoide o micro-servo que despliega 2–4 agujas).

| Efector | Toalla de rizo | Camiseta fina | Coste/complejidad DIY |
| --- | --- | --- | --- |
| Pinza 2 dedos (blanda) | Malo (resbala) | Regular (por el borde) | Bajo |
| **Aguja retráctil** | **Muy bueno** | Bueno | Medio (solenoide + agujas) |
| Ventosa/succión | Malo (poroso) | Malo | Medio |
| Pinza tipo "fin-ray" | Regular | Bueno | Medio (imprimir TPU) |

**Sugerencia:** cabezal con **aguja retráctil** como principal + almohadilla
blanda para el pellizco de prendas finas.

### B) Cambiar la estructura: pórtico cartesiano (gantry) en vez de brazo articulado

Para **pick-and-place sobre una mesa plana**, un **pórtico XYZ (tipo CoreXY /
impresora 3D)** es **más barato, más rígido, más preciso y con más carga útil
efectiva** que un brazo articulado de servos:

| Criterio | Brazo articulado (servos) | **Pórtico XYZ (gantry)** |
| --- | --- | --- |
| Par/carga útil | Cae con el alcance | Alta y constante (no hay palanca) |
| Precisión/repetibilidad | ±6–12 mm (backlash) | ±0.1–0.5 mm (steppers + correa) |
| Rigidez | Baja (voladizo largo) | Alta (estructura cerrada) |
| Cinemática | Trigonometría, calibración | Trivial (X, Y, Z directos) |
| Coste | Servos de par alto = caros | NEMA17 + correa + Arduino = barato |
| Encaje con "el tablero dobla" | Suficiente | **Ideal** (sólo hace falta pick + place) |

Como en nuestra arquitectura **el tablero hace los dobleces**, el manipulador
sólo necesita **bajar, agarrar, subir y soltar centrado**: eso es exactamente lo
que un pórtico hace de maravilla. **El pórtico es la opción de mayor calidad.**

### C) Si se mantiene el brazo articulado, mitigaciones obligatorias

1. **Alcance corto** (menos `L1+L2+L3`): el par baja de forma lineal con `R`.
2. **Contrapeso o resorte de gas** en el hombro (asistencia).
3. **Reducción por engranaje/correa** en el hombro (multiplica el par y reduce
   backlash) o **steppers con reductora** en vez de servos.
4. **No operar en extensión máxima** con carga.
5. **Rótulas sin holgura / rodamientos** en las juntas.

### D) Acotar el alcance de "toalla" en v1

- v1: **camiseta, boxer y toalla de manos/mediana (≤ ~300 g)**.
- Toalla de baño grande: **objetivo posterior**, tras validar el efector.

## Plan de reducción de riesgo (probar antes de comprar todo)

1. **Prueba de agarre temprana (barata):** fabricar sólo el **efector** (aguja o
   pinza) montado en un soporte fijo/manual y comprobar que levanta una toalla
   real de forma repetible **antes** de construir toda la estructura.
2. **Prueba de carga del hombro:** colgar 0.5–0.7 kg a 0.36 m y medir sag/temblor
   del servo elegido; si falla, pasar a reductora o a pórtico.
3. **Decisión de arquitectura** (brazo vs pórtico) **con datos**, no en papel.

## Resumen de la recomendación

> Para el objetivo de **calidad**, la opción recomendada es:
> **pórtico XYZ + cabezal con aguja retráctil**, acotando v1 a prendas ≤ ~300 g.
> El brazo articulado de servos con pinza blanda queda como opción de menor coste
> pero **menor fiabilidad**, sólo viable con las mitigaciones (C) y para toallas
> ligeras.

Esta decisión **no cambia** el resto del sistema: la visión, la clasificación
(software ya funcional) y el **tablero de plegado** siguen igual; sólo cambia el
"cómo se recoge y coloca" la prenda, que es precisamente el módulo más crítico.
