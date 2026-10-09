# s15_keywords_clean.py

from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"


REPLACEMENTS = {
    "NLP APPLICATION": "NLP APPLICATIONS",
    "ARTIFICIAL INTELLIGENCE (AI)": "ARTIFICIAL INTELLIGENCE",
    "BLOCK-CHAIN": "BLOCKCHAIN",
    "BLOCKCHAIN TECHNOLOGY": "BLOCKCHAIN",
}


def s15_keywords_clean() -> None:

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")

    df["keywords_clean"] = df["keywords_raw"].str.upper()
    for old, new in REPLACEMENTS.items():
        df["keywords_clean"] = df["keywords_clean"].str.replace(old, new)

    df.to_csv(SUBMISSION_FILE, index=False)


if __name__ == "__main__":
    s15_keywords_clean()