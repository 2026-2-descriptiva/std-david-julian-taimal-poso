# s10_countries_clusters.py


from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
MATRIX_FILE = SUBMISSION_DIRECTORY / "country_cooc_matrix.csv"
CLUSTERS_FILE = SUBMISSION_DIRECTORY / "country_clusters.txt"


def make_communities_report(input_file, output_file) -> None:

    cooc_matrix = pd.read_csv(input_file)
    cooc_matrix = cooc_matrix.set_index(cooc_matrix.columns[0])

    G = nx.from_pandas_adjacency(cooc_matrix)
    G.remove_edges_from(nx.selfloop_edges(G))
    G.remove_edges_from(
        [(u, v) for u, v, w in G.edges(data="weight") if not w or w <= 0]
    )

    communities = nx.community.louvain_communities(G, weight="weight", seed=0)
    communities = sorted(communities, key=lambda x: len(x), reverse=True)

    with open(output_file, "w") as f:

        for community in communities:
            community = "; ".join(sorted(community))
            f.write(f"{community}\n")


def s10_countries_clusters():
    make_communities_report(
        input_file=MATRIX_FILE,
        output_file=CLUSTERS_FILE,
    )


if __name__ == "__main__":
    s10_countries_clusters()