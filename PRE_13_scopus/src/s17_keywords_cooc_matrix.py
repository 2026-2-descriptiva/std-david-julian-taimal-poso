# s17_keywords_cooc_matrix.py

from pathlib import Path

from s08_countries_cooc_matrix import make_cooc_matrix

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
MATRIX_FILE = SUBMISSION_DIRECTORY / "keywords_cooc_matrix.csv"


def s17_keywords_cooc_matrix():
    make_cooc_matrix(
        column="keywords_clean",
        output_file=MATRIX_FILE,
    )


if __name__ == "__main__":
    s17_keywords_cooc_matrix()