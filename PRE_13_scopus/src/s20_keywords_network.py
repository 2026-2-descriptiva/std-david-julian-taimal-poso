# s20_keywords_network.py

from pathlib import Path

from s11_countries_network import make_cooc_network_plot

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"

CLUSTERS_FILE = SUBMISSION_DIRECTORY / "keywords_clusters.txt"
MATRIX_FILE = SUBMISSION_DIRECTORY / "keywords_cooc_matrix.csv"
FREQUENCY_REPORT_FILE = SUBMISSION_DIRECTORY / "keywords_frequency.csv"

NETWORK_FILE = SUBMISSION_DIRECTORY / "keywords_cooc_network.html"

FONTSIZE = 12


def s20_keywords_network():
    make_cooc_network_plot(
        matrix_file=MATRIX_FILE,
        clusters_file=CLUSTERS_FILE,
        frequency_report_file=FREQUENCY_REPORT_FILE,
        output_file=NETWORK_FILE,
        node_size_range=(10, 100),
        font_size_range=(8, 30),
        link_size_range=(1, 10),
    )


if __name__ == "__main__":
    s20_keywords_network()