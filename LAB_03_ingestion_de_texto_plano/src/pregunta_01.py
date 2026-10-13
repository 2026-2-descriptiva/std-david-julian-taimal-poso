from pathlib import Path
import re
import pandas as pd


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    filepath = Path("data/clusters_report.txt")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"

    lines = filepath.read_text(encoding="utf-8").splitlines()

    content_lines = []
    start = False
    for line in lines:
        if line.startswith("----"):
            start = True
            continue
        if start:
            content_lines.append(line)

    clusters = []
    curr = None

    for line in content_lines:
        m = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$", line)
        if m:
            if curr:
                clusters.append(curr)
            c_num = int(m.group(1))
            c_qty = int(m.group(2))
            c_pct = float(m.group(3).replace(",", "."))
            kw_part = m.group(4)
            curr = {
                "cluster": c_num,
                "cantidad_de_palabras_clave": c_qty,
                "porcentaje_de_palabras_clave": c_pct,
                "kw": [kw_part],
            }
        elif curr and line.strip():
            curr["kw"].append(line.strip())

    if curr:
        clusters.append(curr)

    for c in clusters:
        full_kw = " ".join(c["kw"])
        full_kw = " ".join(full_kw.split())
        if full_kw.endswith("."):
            full_kw = full_kw[:-1]
        c["principales_palabras_clave"] = full_kw
        del c["kw"]

    return pd.DataFrame(clusters)
