# s02_make_documents_by_year_plot.py

from pathlib import Path

import pandas as pd
import plotly.express as px  # pyright: ignore[reportMissingImports]

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"
PLOT_FILE = SUBMISSION_DIRECTORY / "documents_by_year.html"


def s02_make_documents_by_year_plot():

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")

    df = df[["publication_year"]].copy()
    df = df.groupby("publication_year").size().reset_index(name="count")

    all_years = pd.DataFrame(
        {
            "publication_year": range(
                int(df["publication_year"].min()), int(df["publication_year"].max()) + 1
            )
        }
    )
    df = all_years.merge(df, on="publication_year", how="left")
    df["count"] = df["count"].fillna(0).astype(int)

    fig = px.line(
        df,
        x="publication_year",
        y="count",
        labels={"publication_year": "Año", "count": "Documentos"},
        title="Documentos por año",
        markers=True,
    )
    fig.update_xaxes(dtick=1, tickangle=270, showline=True, linecolor="black")
    fig.update_yaxes(showline=True, linecolor="black")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    fig.write_html(PLOT_FILE)


if __name__ == "__main__":
    s02_make_documents_by_year_plot()
