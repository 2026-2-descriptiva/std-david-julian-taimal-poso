# s14_keywords_create.py

from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"


def s14_keywords_create() -> None:

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")
    df["keywords_raw"] = (
        df["author_keywords"].fillna("") + "; " + df["index_keywords"].fillna("")
    )
    df["keywords_raw"] = df["keywords_raw"].str.strip("; ")
    df.to_csv(SUBMISSION_FILE, index=False)


if __name__ == "__main__":
    s14_keywords_create()
