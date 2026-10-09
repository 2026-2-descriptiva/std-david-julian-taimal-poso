# s08_countries_cooc_matrix.py

from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
MATRIX_FILE = SUBMISSION_DIRECTORY / "country_cooc_matrix.csv"


def make_cooc_matrix(column, output_file) -> pd.DataFrame:

    df = pd.read_csv(DATA_FILE, compression="gzip")

    df = df[[column]].copy()
    df = df.rename(columns={column: "rows"})
    df["columns"] = df["rows"]

    df = df.dropna()

    df["rows"] = df["rows"].str.split("; ")
    df["columns"] = df["columns"].str.split("; ")
    df = df.explode("rows")
    df = df.explode("columns")
    matrix_list = df.groupby(["rows", "columns"]).size().reset_index(name="count")

    matrix = (
        matrix_list.pivot(index="rows", columns="columns", values="count")
        .fillna(0)
        .astype(int)
    )

    matrix.to_csv(output_file)
    return matrix


def s08_countries_cooc_matrix():
    make_cooc_matrix(
        column="countries_clean",
        output_file=MATRIX_FILE,
    )


if __name__ == "__main__":
    s08_countries_cooc_matrix()