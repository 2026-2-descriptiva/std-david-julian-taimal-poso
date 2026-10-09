# s05_countries_frequency_report.py


from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
FREQUENCY_REPORT_FILE = SUBMISSION_DIRECTORY / "country_frequency.csv"


def make_frequency_report(column, file_path):

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")
    df = df[[column]].copy()
    df = df.rename(columns={column: "item"})

    series = df["item"].copy()
    series = series.dropna()
    series = series.str.split("; ").explode()
    series = series.value_counts()
    series.to_csv(file_path)


def s05_countries_frequency_report():
    make_frequency_report(
        column="countries_clean",
        file_path=FREQUENCY_REPORT_FILE,
    )


if __name__ == "__main__":
    s05_countries_frequency_report()