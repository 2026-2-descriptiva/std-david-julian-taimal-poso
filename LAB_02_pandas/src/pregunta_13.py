from pathlib import Path
import pandas as pd


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    filepath_0 = Path("data/tbl0.tsv")
    if not filepath_0.exists():
        filepath_0 = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    filepath_2 = Path("data/tbl2.tsv")
    if not filepath_2.exists():
        filepath_2 = Path(__file__).resolve().parents[1] / "data" / "tbl2.tsv"

    tbl0 = pd.read_csv(filepath_0, sep="\t")
    tbl2 = pd.read_csv(filepath_2, sep="\t")

    merged = pd.merge(tbl0, tbl2, on="c0")
    return merged.groupby("c1")["c5b"].sum()
