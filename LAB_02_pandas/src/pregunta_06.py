from pathlib import Path
import pandas as pd


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    filepath = Path("data/tbl1.tsv")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"

    df = pd.read_csv(filepath, sep="\t")
    return sorted(df["c4"].str.upper().unique().tolist())
