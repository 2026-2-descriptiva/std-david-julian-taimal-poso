# Rentabilidad de ventas

## Propósito

Diagnosticar si las ventas de una cadena de suministros de oficina generan utilidad, identificar dónde se concentran las pérdidas y evaluar el efecto de los descuentos sobre el margen.

## Competencia

Define indicadores de rentabilidad con sus denominadores correctos, distingue entre volumen de ventas y utilidad, y prioriza segmentos por el dinero que pierden, considerando un volumen mínimo.

## Datos

`data/superstore_orders.csv.gz` contiene 1.952 líneas de pedido con sus ventas, utilidad, descuento, segmento del cliente, categoría del producto y otros atributos del pedido. El archivo está comprimido con gzip, usa punto y coma (`;`) como separador y coma (`,`) como separador decimal.

## Restricciones

- Use Pandas para cargar y transformar los datos.
- No modifique el archivo de `data/` ni los archivos de `tests/`.
- Escriba su solución en la función `pregunta_01()` de `src/pregunta_01.py`; las pruebas ejecutan esa función.
- Los entregables son los tres archivos CSV indicados en la pregunta, en `submission/`.
