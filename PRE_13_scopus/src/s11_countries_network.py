# s11_countries_network.py


from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"

CLUSTERS_FILE = SUBMISSION_DIRECTORY / "country_clusters.txt"
MATRIX_FILE = SUBMISSION_DIRECTORY / "country_cooc_matrix.csv"
FREQUENCY_REPORT_FILE = SUBMISSION_DIRECTORY / "country_frequency.csv"

NETWORK_FILE = SUBMISSION_DIRECTORY / "country_collab_network.html"

FONTSIZE = 12


def _create_networkx_graph(matrix_file) -> nx.Graph:

    cooc_matrix = pd.read_csv(matrix_file)
    cooc_matrix = cooc_matrix.set_index(cooc_matrix.columns[0])

    G = nx.from_pandas_adjacency(cooc_matrix)
    G.remove_edges_from(nx.selfloop_edges(G))
    G.remove_edges_from(
        [(u, v) for u, v, w in G.edges(data="weight") if not w or w <= 0]
    )
    G.remove_nodes_from(list(nx.isolates(G)))

    return G


def _assign_cluster_to_node(G, clusters_file) -> dict:

    with open(clusters_file, "r") as f:
        communities = [line.strip().split("; ") for line in f.readlines()]

    node_to_cluster = {
        node: cluster_id
        for cluster_id, community in enumerate(communities)
        for node in community
    }

    nx.set_node_attributes(G, node_to_cluster, "cluster")

    return G


def _assign_node_occurrences(G, frequency_report_file) -> nx.Graph:

    country_frequency = pd.read_csv(frequency_report_file)
    country_frequency = country_frequency.set_index(country_frequency.columns[0])

    node_sizes = {
        node: (
            country_frequency.loc[node].values[0]
            if node in country_frequency.index
            else 1
        )
        for node in G.nodes()
    }

    nx.set_node_attributes(G, node_sizes, "occ")

    return G


def _assign_node_colors(G) -> nx.Graph:

    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ] * 10

    cluster_colors = {
        cluster_id: palette[cluster_id % len(palette)]
        for cluster_id in set(nx.get_node_attributes(G, "cluster").values())
    }

    node_colors = {node: cluster_colors[G.nodes[node]["cluster"]] for node in G.nodes()}

    nx.set_node_attributes(G, node_colors, "color")

    return G


def _assign_node_sizes(G, frequency_report_file, node_size_range) -> nx.Graph:

    min_size = node_size_range[0]
    max_size = node_size_range[1]

    frequency = pd.read_csv(frequency_report_file)
    frequency = frequency.set_index(frequency.columns[0])

    occ = {node: G.nodes[node]["occ"] for node in G.nodes()}

    if max_size == min_size:

        scaled_sizes = {node: ((min_size + max_size) / 2) for node in occ}

    else:

        min_node_size = min(occ.values())
        max_node_size = max(occ.values())
        node_size_range = max_node_size - min_node_size

        scaled_sizes = {
            node: min_size
            + (max_size - min_size) * ((s - min_node_size) / node_size_range) ** 0.5
            for node, s in occ.items()
        }

    nx.set_node_attributes(G, scaled_sizes, "size")

    return G


def _asssign_link_sizes(G, link_size_range) -> nx.Graph:

    min_size = link_size_range[0]
    max_size = link_size_range[1]

    weights = {edge: G.edges[edge]["weight"] for edge in G.edges()}

    if max_size == min_size:

        scaled_sizes = {edge: ((min_size + max_size) / 2) for edge in weights}

    else:

        min_weight = min(weights.values())
        max_weight = max(weights.values())
        weight_range = max_weight - min_weight

        scaled_sizes = {
            edge: min_size
            + (max_size - min_size) * ((w - min_weight) / weight_range) ** 0.5
            for edge, w in weights.items()
        }

    nx.set_edge_attributes(G, scaled_sizes, "width")

    return G


def _assign_font_sizes(G, font_size_range) -> nx.Graph:

    min_font_size = font_size_range[0]
    max_font_size = font_size_range[1]

    node_sizes = {node: G.nodes[node]["size"] for node in G.nodes()}

    if max_font_size == min_font_size:

        scaled_font_sizes = {
            node: ((min_font_size + max_font_size) / 2) for node in node_sizes
        }

    else:

        min_node_size = min(node_sizes.values())
        max_node_size = max(node_sizes.values())
        node_size_range = max_node_size - min_node_size
        font_range = max_font_size - min_font_size

        scaled_font_sizes = {
            node: min_font_size
            + font_range * ((s - min_node_size) / node_size_range) ** 0.5
            for node, s in node_sizes.items()
        }

    nx.set_node_attributes(G, scaled_font_sizes, "font_size")

    return G


def _make_edge_trace(G, pos) -> list[go.Scatter]:

    edge_traces = []

    for u, v in G.edges():
        edge_traces.append(
            go.Scatter(
                x=[pos[u][0], pos[v][0]],
                y=[pos[u][1], pos[v][1]],
                mode="lines",
                line=dict(color="gray", width=G.edges[u, v]["width"]),
                hoverinfo="none",
            )
        )

    return edge_traces


def _make_node_trace(G, pos) -> go.Scatter:

    node_x, node_y = [], []

    for node in G.nodes():
        node_x.append(pos[node][0])
        node_y.append(pos[node][1])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(G.nodes()),
        textposition="middle center",
        textfont=dict(
            size=[G.nodes[node]["font_size"] for node in G.nodes()],
            color="black",
        ),
        hovertext=[
            f"{node}<br>Frequency: {G.nodes[node]['size']}" for node in G.nodes()
        ],
        hoverinfo="text",
        marker=dict(
            size=[G.nodes[node]["size"] for node in G.nodes()],
            color=[G.nodes[node]["color"] for node in G.nodes()],
            line=dict(width=1, color="black"),
            opacity=0.5,
        ),
    )

    return node_trace


def make_cooc_network_plot(
    matrix_file,
    clusters_file,
    frequency_report_file,
    output_file,
    node_size_range,
    font_size_range,
    link_size_range,
):
    G = _create_networkx_graph(matrix_file)
    G = _assign_cluster_to_node(G, clusters_file)
    G = _assign_node_occurrences(G, frequency_report_file)
    G = _assign_node_colors(G)
    G = _assign_node_sizes(G, frequency_report_file, node_size_range)
    G = _assign_font_sizes(G, font_size_range)
    G = _asssign_link_sizes(G, link_size_range)

    pos = nx.spring_layout(G, seed=1, k=1.35, iterations=200)

    edge_trace = _make_edge_trace(G, pos)
    node_trace = _make_node_trace(G, pos)

    figure = go.Figure(data=[*edge_trace, node_trace])

    figure.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    figure.write_html(output_file)


def s11_countries_network():
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
    s11_countries_network()
