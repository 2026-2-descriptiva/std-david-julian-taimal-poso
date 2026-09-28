# Tiempos de respuesta de PQRS

## Propósito

Medir si una entidad pública responde las peticiones, quejas, reclamos y sugerencias (PQRS) dentro del plazo legal, comparando canales y años, y sin ignorar las solicitudes que siguen pendientes.

## Competencia

Construye un indicador de cumplimiento a partir de fechas, elige la unidad de tiempo que corresponde a la regla del negocio (días hábiles o calendario), trata correctamente los casos sin respuesta y comunica cómo cambia la conclusión según esas decisiones.

## Datos

`data/historical_requests_web.csv.gz` y `data/historical_requests_letter.csv.gz` contienen las solicitudes recibidas entre 2016 y 2021 por la página web y por carta, con sus fechas de entrada y de respuesta. Los archivos están comprimidos con gzip; Pandas puede leerlos directamente.

## Restricciones

- Use Pandas para cargar y transformar los datos.
- No modifique los archivos de `data/` ni los archivos de `tests/`.
- Escriba su solución en la función `pregunta_01()` de `src/pregunta_01.py`; las pruebas ejecutan esa función.
- Los entregables son los tres archivos CSV indicados en la pregunta, en `submission/`.
