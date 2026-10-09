# s07_countries_world_map.py

from pathlib import Path

import folium
import pandas as pd

SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"
DATA_FILE = SUBMISSION_DIRECTORY / "country_frequency.csv"
WORLD_MAP_FILE = SUBMISSION_DIRECTORY / "world_map.html"

GEO_DATA_URL = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"


def s07_countries_world_map() -> None:

    df = pd.read_csv(DATA_FILE)

    m = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles=None,
    )

    folium.Choropleth(
        geo_data=GEO_DATA_URL,
        data=df,
        columns=["item", "count"],
        key_on="feature.properties.name",
        fill_color="Greens",
    ).add_to(m)

    m.save(WORLD_MAP_FILE)


if __name__ == "__main__":
    s07_countries_world_map()