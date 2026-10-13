from collections import defaultdict
import gzip
from pathlib import Path


def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    filepath = Path("data/data.csv.gz")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    totals = defaultdict(int)
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                totals[parts[0]] += int(parts[1])
    return sorted(totals.items())
