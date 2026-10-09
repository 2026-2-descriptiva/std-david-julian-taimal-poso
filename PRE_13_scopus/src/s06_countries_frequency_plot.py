# s06_countries_frequency_plot.py


from pathlib import Path

import pandas as pd
import plotly.express as px

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "country_frequency.csv"
BAR_PLOT_FILE = SUBMISSION_DIRECTORY / "country_frequency_plot.html"


def make_frequency_plot(filepath, n):

    df = pd.read_csv(filepath)
    df = df.head(n)

    fig = px.bar(
        df,
        x=df.columns[1],
        y=df.columns[0],
        orientation="h",
    )
    fig.update_yaxes(autorange="reversed")
    fig.write_html(BAR_PLOT_FILE)


def s06_countries_frequency_plot():
    make_frequency_plot(DATA_FILE, n=10)


if __name__ == "__main__":
    s06_countries_frequency_plot()
    
    