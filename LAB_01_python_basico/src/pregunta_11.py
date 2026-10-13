from collections import defaultdict
import gzip
from pathlib import Path


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """
    filepath = Path("data/data.csv.gz")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    totals = defaultdict(int)
    with gzip.open(filepath, "rt", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                val = int(parts[1])
                for code in parts[3].split(","):
                    if code:
                        totals[code] += val

    return dict(sorted(totals.items()))
