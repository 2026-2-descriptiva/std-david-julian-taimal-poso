# s13_authors_frequency_report.py



from pathlib import Path

import pandas as pd
from s05_countries_frequency_report import make_frequency_report

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
REPORT_FREQUENCY_FILE = SUBMISSION_DIRECTORY / "authors_frequency.csv"


def s13_authors_frequency_report():
    make_frequency_report(
        column="author_full_names",
        file_path=REPORT_FREQUENCY_FILE,
    )


if __name__ == "__main__":
    s13_authors_frequency_report()