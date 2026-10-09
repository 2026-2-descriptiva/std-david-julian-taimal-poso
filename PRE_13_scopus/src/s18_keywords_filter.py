# s18_keywords_filter.py



from pathlib import Path

import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
MATRIX_FILE = SUBMISSION_DIRECTORY / "keywords_cooc_matrix.csv"


def filter_cooc_matrix(matrix_file, min_occ):

    terms = []

    df = pd.read_csv(matrix_file)
    df = df.set_index(df.columns[0])

    diagonal = df.values.diagonal()
    for i, term in enumerate(df.index):
        if diagonal[i] >= min_occ:
            terms.append(term)

    df = df.loc[terms, terms]

    df.to_csv(MATRIX_FILE, index=True)


def s18_keywords_filter():
    filter_cooc_matrix(
        matrix_file=MATRIX_FILE,
        min_occ=10,
    )


if __name__ == "__main__":
    s18_keywords_filter()