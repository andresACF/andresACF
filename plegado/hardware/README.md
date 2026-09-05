# Dobla Hardware — estación de plegado para uso diario

Sistema físico semi-automático: colocas la prenda abierta, pulsas un botón
(o la web), la tabla la dobla y la vuelca a una canasta.

No es un robot con visión artificial. Es una **tabla de pliegue motorizada**
(estilo FlipFold) con 4 servos. Es lo más realista de construir en casa para
usar todos los días sin gastar miles de dólares.

## Flujo de uso diario

1. Sacas la prenda de la secadora / tendedero.
2. La extiendes centrada sobre la tabla.
3. Pulsas **Doblar** (botón físico o app).
4. Los paneles pliegan: izquierda → derecha → inferior.
5. La tabla se inclina y la prenda cae en la canasta.
6. La tabla vuelve a posición. Siguiente prenda.

Tiempo típico por prenda: **8–12 segundos** + el tiempo de colocarla.

## Qué sí / qué no

| Bien | Mal / no confiable |
|------|--------------------|
| Camisetas, polos | Sábanas ajustadas |
| Toallas medianas | Abrigos gruesos |
| Pantalones deportivos / jeans finos | Prendas con mucho volumen |
| Fundas de almohada | Ropa muy húmeda |

Regla de oro: si no cabe plana en la tabla (~45 × 55 cm), no la fuerces.

## Arquitectura

```
  [Botón / Web Serial]
           │
        ESP32
           │
    ┌──────┼──────────┐
  ServoL ServoR ServoB ServoTip
    │      │      │       │
  panel  panel  panel   bascula
  izq.   der.   abajo   → canasta
```

## Carpetas

| Ruta | Contenido |
|------|-----------|
| [`BOM.md`](./BOM.md) | Lista de materiales y costo estimado |
| [`MONTAJE.md`](./MONTAJE.md) | Corte, ensamble, cableado, calibración |
| [`USO_DIARIO.md`](./USO_DIARIO.md) | Rutina diaria, atascos y mantenimiento |
| [`../firmware/dobla_fold/`](../firmware/dobla_fold/) | Código Arduino para ESP32 |
| [`../index.html`](../index.html) | UI + control por Web Serial |

## Seguridad

- Fuente de 5 V con capacidad real (mín. 5 A). Los servos pican corriente.
- No metas la mano mientras pliega.
- Fija la canasta para que no se vuelque al recibir la prenda.
- Si un servo forcejea, corta energía: suele ser prenda mal colocada.
