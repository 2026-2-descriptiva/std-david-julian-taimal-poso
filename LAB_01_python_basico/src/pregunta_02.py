from collections import defaultdict
import gzip
from pathlib import Path


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    filepath = Path("data/data.csv.gz")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    counts = defaultdict(int)
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if parts and parts[0]:
                counts[parts[0]] += 1
    return sorted(counts.items())
