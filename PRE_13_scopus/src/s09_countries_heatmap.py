# s09_countries_heatmap.py

from pathlib import Path

import pandas as pd
import plotly.express as px

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
MATRIX_FILE = SUBMISSION_DIRECTORY / "country_cooc_matrix.csv"
COOC_HEATMAP_FILE = SUBMISSION_DIRECTORY / "country_cooc_heatmap.html"


def make_cooc_heatmap(input_file, output_file) -> None:

    cooc_matrix = pd.read_csv(input_file)
    cooc_matrix = cooc_matrix.set_index(cooc_matrix.columns[0])

    figure = px.imshow(
        cooc_matrix,
        color_continuous_scale="Blues",
    )

    text = cooc_matrix.map(lambda value: str(value) if value > 0 else "").to_numpy()
    figure.update_traces(text=text, texttemplate="%{text}", textfont_size=9)

    figure.update_traces(xgap=1, ygap=1)
    figure.update_coloraxes(showscale=False)

    n_rows, n_cols = cooc_matrix.shape

    figure.update_xaxes(
        side="top",
        layer="above traces",
        tickangle=270,
        showgrid=True,
        range=[-0.5, n_cols - 0.5],
    )

    figure.update_yaxes(
        layer="above traces",
        showgrid=True,
        scaleanchor="x",
        scaleratio=1,
        range=[n_rows - 0.5, -0.5],
    )

    figure.write_html(output_file)


def s09_countries_heatmap():
    make_cooc_heatmap(
        input_file=MATRIX_FILE,
        output_file=COOC_HEATMAP_FILE,
    )


if __name__ == "__main__":
    s09_countries_heatmap()