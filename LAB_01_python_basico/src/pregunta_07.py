from collections import defaultdict
import gzip
from pathlib import Path


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """
    filepath = Path("data/data.csv.gz")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    values = defaultdict(list)
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                values[int(parts[1])].append(parts[0])

    return sorted(values.items())
