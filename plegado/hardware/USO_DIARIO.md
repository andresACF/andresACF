# Uso diario de Dobla

Guía corta para cuando la máquina ya está armada y calibrada.

## Encendido (cada sesión)

1. Enchufa la **fuente 5 V 10 A** (servos).
2. Conecta el **ESP32** por USB (PC) o su propio cargador 5 V 1 A.
3. Espera `DOBLA_READY` en el Monitor Serial o el LED apagado = listo.
4. Opcional: abre `plegado/index.html` en Chrome/Edge → **Conectar ESP32**.

## Flujo por prenda

1. Extiende la prenda **centrada** en la tabla (cuello hacia el panel inferior).
2. Pulsa el **botón físico** o **Doblar en hardware** en la web.
3. No toques hasta que termine el ciclo (~8–12 s).
4. La prenda cae en la canasta. Repite.

## Si se atasca

1. Corta la fuente 5 V de los servos.
2. Saca la prenda con la mano.
3. Enciende de nuevo y envía `HOME` (web o Monitor Serial).
4. Revisa que la prenda no sea demasiado gruesa/grande.

## Qué doblar hoy

- Sí: camisetas, polos, toallas medianas, pantalones finos/deportivos, fundas.
- No: sábanas ajustadas, abrigos, jeans muy rígidos, ropa mojada.

## Mantenimiento semanal

- Revisa tornillos de bielas y bisagras.
- Limpia pelusa de la tabla.
- Escucha ruidos raros en servos: suele ser ángulo mal calibrado o prenda mal puesta.

## Checklist “listo para diario”

- [ ] 10 camisetas seguidas sin atasco
- [ ] Canasta fija y no se vuelca
- [ ] Botón físico funciona sin PC
- [ ] Web Serial funciona cuando quieres control desde el navegador
- [ ] Sabes apagar la fuente en emergencias
