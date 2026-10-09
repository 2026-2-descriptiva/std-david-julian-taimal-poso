# s03_countries_create.py

from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"


def _create_countries_column(df):

    df = df.copy()
    df["countries_raw"] = df["affiliations"].copy()
    df["countries_raw"] = df["countries_raw"].str.split(";")
    df["countries_raw"] = df["countries_raw"].map(
        lambda x: [y.split(",") for y in x] if isinstance(x, list) else x
    )
    df["countries_raw"] = df["countries_raw"].map(
        lambda x: [y[-1].strip() for y in x] if isinstance(x, list) else x
    )
    df["countries_raw"] = df["countries_raw"].map(
        lambda x: set(x) if isinstance(x, list) else x
    )
    df["countries_raw"] = df["countries_raw"].str.join("; ")

    return df


def s03_countries_create() -> None:

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")
    df = _create_countries_column(df)
    print(df.countries_raw.head(20))
    df.to_csv(SUBMISSION_FILE, index=False, compression="gzip")


if __name__ == "__main__":
    s03_countries_create()