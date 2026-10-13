from pathlib import Path
import numpy as np
import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    activity_dir = Path(__file__).resolve().parents[1]
    data_dir = activity_dir / "data"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(data_dir.glob("bank-marketing-campaing-*.csv.gz"))
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    df = df.sort_values("client_id").reset_index(drop=True)

    # 1. client
    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()
    client["job"] = (
        client["job"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    client["education"] = client["education"].astype(str).str.replace(
        ".", "_", regex=False
    )
    client["education"] = client["education"].replace("unknown", np.nan)
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # 2. campaign
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
        ]
    ].copy()
    campaign["previous_outcome"] = (
        campaign["previous_outcome"] == "success"
    ).astype(int)
    campaign["campaign_outcome"] = (
        campaign["campaign_outcome"] == "yes"
    ).astype(int)

    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }
    campaign["last_contact_date"] = (
        "2022-"
        + df["month"].str.lower().map(month_map)
        + "-"
        + df["day"].astype(str).str.zfill(2)
    )

    # 3. economics
    economics = df[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].copy()

    client.to_csv(submission_dir / "client.csv", index=False)
    campaign.to_csv(submission_dir / "campaign.csv", index=False)
    economics.to_csv(submission_dir / "economics.csv", index=False)

    return client, campaign, economics
