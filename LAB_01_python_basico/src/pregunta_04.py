from collections import defaultdict
import gzip
from pathlib import Path


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    filepath = Path("data/data.csv.gz")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    counts = defaultdict(int)
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                month = parts[2].split("-")[1]
                counts[month] += 1
    return sorted(counts.items())
