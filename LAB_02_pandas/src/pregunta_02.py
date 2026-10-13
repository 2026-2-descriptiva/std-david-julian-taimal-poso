from pathlib import Path
import pandas as pd


def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """
    filepath = Path("data/tbl0.tsv")
    if not filepath.exists():
        filepath = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    df = pd.read_csv(filepath, sep="\t")
    return len(df.columns)
