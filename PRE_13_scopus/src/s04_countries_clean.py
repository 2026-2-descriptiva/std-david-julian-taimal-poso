from pathlib import Path

import pandas as pd
import requests

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
SUBMISSION_FILE = SUBMISSION_DIRECTORY / "scopus.csv.gz"

REPLACEMENTS = {
    "North Macedonia": "Macedonia",
    "Palestine": "West Bank",
    "Russian Federation": "Russia",
    "Serbia": "Republic of Serbia",
    "USA": "United States of America",
    "United States": "United States of America",
    "Viet Nam": "Vietnam",
}


URL = (
    "https://raw.githubusercontent.com/python-visualization/"
    "folium/master/examples/data/world-countries.json"
)


VALID_COUNTRIES = {
    feature["properties"]["name"] for feature in requests.get(URL).json()["features"]
}


def _correct_country_names(df):

    df = df.copy()

    df["countries_clean"] = df["countries_clean"].str.split("; ")
    df["countries_clean"] = df["countries_clean"].map(
        lambda x: (
            [REPLACEMENTS.get(y, y) for y in x] if isinstance(x, list) else x
        )
    )
    df["countries_clean"] = df["countries_clean"].map(
        lambda x: set(x) if isinstance(x, list) else x
    )
    df["countries_clean"] = df["countries_clean"].str.join("; ")

    return df


def _remove_invalid_countries(df):

    df = df.copy()
    df["countries_clean"] = df["countries_clean"].str.split("; ")
    df["countries_clean"] = df["countries_clean"].map(
        lambda x: [y for y in x if y in VALID_COUNTRIES] if isinstance(x, list) else x
    )
    df["countries_clean"] = df["countries_clean"].str.join("; ")
    return df


def s04_countries_clean() -> None:

    df = pd.read_csv(SUBMISSION_FILE, compression="gzip")

    df["countries_clean"] = df["countries_raw"]
    df = _correct_country_names(df)
    df = _remove_invalid_countries(df)
    df.to_csv(SUBMISSION_FILE, index=False, compression="gzip")


if __name__ == "__main__":
    s04_countries_clean()
