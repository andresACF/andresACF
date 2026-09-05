# Montaje paso a paso

Tiempo estimado de construcción: un fin de semana si ya tienes herramientas.

## 1. Cortar la tabla

Dimensiones recomendadas (ajusta a tu ropa):

| Pieza | Ancho × Alto |
|-------|--------------|
| Base fija | 45 × 55 cm |
| Panel izquierdo | 15 × 55 cm |
| Panel derecho | 15 × 55 cm |
| Panel inferior | 45 × 18 cm |

```
┌─────┬──────────┬─────┐
│ Izq │   Base   │ Der │   ← bisagras verticales
│15cm │   45cm   │15cm │
├─────┴──────────┴─────┤
│      Inferior 18cm   │   ← bisagra horizontal
└──────────────────────┘
```

1. Corta el MDF.
2. Lija bordes.
3. Barniza o pinta (impermeabiliza).
4. Coloca bisagras: izquierda y derecha abren hacia el centro; inferior hacia arriba.

## 2. Marco basculante

La base + paneles van montados sobre un **marco basculante** que rota ~45–60°
hacia la canasta.

```
  Vista lateral:

  [tabla horizontal]
       │ bisagra marco
       ●────────────  → se inclina
      /|
     / | soporte fijo
    /  |
   ■ mesa / patas     ■ canasta
```

- El eje de bascula va en el borde cercano a la canasta.
- Un servo (`ServoTip`) empuja/tira el marco con una biela.
- La canasta queda pegada al borde, ligeramente más baja que la tabla.

## 3. Instalar servos

| Servo | Pin ESP32 | Movimiento |
|-------|-----------|------------|
| `ServoL` | GPIO 18 | Cierra panel izquierdo sobre la base |
| `ServoR` | GPIO 19 | Cierra panel derecho |
| `ServoB` | GPIO 21 | Cierra panel inferior |
| `ServoTip` | GPIO 22 | Inclina el marco hacia la canasta |

Montaje mecánico:

1. Fija cada servo al marco (soportes en L o impresión 3D).
2. Conecta el brazo del servo a una varilla M3 / biela.
3. El otro extremo de la biela va al panel (horquilla + tornillo).
4. En posición “abierto”, el brazo debe tener margen; en “cerrado”, el panel queda plano sobre la base.

Calibra ángulos en el firmware (`ANGLE_L_OPEN`, `ANGLE_L_CLOSED`, etc. en `dobla_fold.ino`) hasta que pliegue sin forzar.

## 4. Cableado

```
Fuente 5V 10A ──┬── VIN servos (rojo en paralelo)
                ├── GND servos ──┬── GND ESP32
                │                │
                └── (NO al 5V del ESP32)

ESP32 5V/USB ← solo el micro (PC o cargador 5V 1A)

Señales:
  GPIO18 → ServoL señal (naranja/amarillo)
  GPIO19 → ServoR
  GPIO21 → ServoB
  GPIO22 → ServoTip
  GPIO23 ← botón Doblar (a GND, INPUT_PULLUP)
  GPIO25 → LED estado (+ resistencia 220Ω a GND)
```

**Importante**

- GND común entre fuente y ESP32.
- Capacitor 1000 µF cerca de los servos (polaridad correcta).
- Nunca alimentes 4 MG996R desde el USB del PC.

## 5. Canasta

1. Coloca la canasta alineada con el borde de volcado.
2. Fíjala (cinta de doble cara fuerte, tornillos al mueble, o un tope de madera).
3. Prueba con una toalla enrollada antes de ropa real.

## 6. Carga del firmware

1. Instala [Arduino IDE](https://www.arduino.cc/) o PlatformIO.
2. Añade soporte ESP32 (board manager) y la librería **ESP32Servo**.
3. Abre `plegado/firmware/dobla_fold/dobla_fold.ino`.
4. Selecciona tu placa ESP32 Dev Module, puerto COM/tty.
5. Sube el sketch.
6. Abre el Monitor Serial a **115200** baudios.

Comandos seriales útiles:

```
FOLD    → ciclo completo
HOME    → abrir paneles + tabla plana
STATUS  → estado actual
```

## 7. Calibración (imprescindible)

1. Sube el firmware.
2. Envía `HOME` y verifica que todo esté abierto y plano.
3. Ajusta `ANGLE_L_OPEN/CLOSED`, etc. de 5° en 5° hasta que:
   - Cierre completo sin rechinar
   - No quede un hueco grande en el pliegue
4. Prueba `FOLD` con una camiseta vieja.
5. Ajusta `TIP_ANGLE` para que caiga en la canasta, no al piso.
6. Ajusta delays (`DELAY_BETWEEN_FOLDS`, `DELAY_TIP`) si va muy rápido/lento.

## 8. Uso diario recomendado

1. Enciende la fuente 5 V, luego el ESP32.
2. Espera el LED: apagado = listo.
3. Coloca la prenda **centrada**, sin arrugas grandes, cuello hacia el panel inferior.
4. Pulsa el botón (o “Doblar en hardware” en la web).
5. No toques hasta que el LED se apague.
6. Si se atasca: apaga la fuente, libera la prenda, `HOME`.

## Checklist de aceptación

- [ ] Una camiseta queda doblada y dentro de la canasta
- [ ] Tres prendas seguidas sin atasco
- [ ] Botón físico y Web Serial disparan el mismo ciclo
- [ ] Al cortar energía y volver, `HOME` deja la tabla usable
- [ ] La canasta no se mueve al recibir la carga

## Si quieres la v2 más adelante

- Sensor IR / fin de carrera para detectar “prenda colocada”
- Perfiles por tipo de prenda (más/menos ángulo)
- Bandeja deslizante en vez de bascula
- App Bluetooth (ESP32 BLE) para no depender del USB
