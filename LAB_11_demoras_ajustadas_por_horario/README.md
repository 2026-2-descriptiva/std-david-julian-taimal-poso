# Demoras ajustadas por horario

## Propósito

Comparar el desempeño de las aerolíneas en puntualidad sin confundir la calidad de su operación con el efecto de los horarios en que vuelan.

## Competencia

Identifica un efecto de composición en una comparación entre grupos, construye un indicador ajustado mediante estandarización indirecta y explica en qué cambia la conclusión frente al indicador sin ajustar.

## Datos

`data/flights_by_carrier_day_hour.csv.gz` contiene los vuelos nacionales entre 2006 y 2008, agregados por año, mes, día de la semana, hora programada de salida y aerolínea, con los vuelos programados, cancelados, operados y demorados. El archivo está comprimido con gzip; Pandas puede leerlo directamente.

## Restricciones

- Use Pandas para cargar y transformar los datos.
- No modifique el archivo de `data/` ni los archivos de `tests/`.
- Escriba su solución en la función `pregunta_01()` de `src/pregunta_01.py`; las pruebas ejecutan esa función.
- Los entregables son los dos archivos CSV indicados en la pregunta, en `submission/`.
