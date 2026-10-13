from pathlib import Path
import numpy as np
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    La función también debe retornar las tres tablas, en el mismo orden.
    """
    activity_dir = Path(__file__).resolve().parents[1]
    data_dir = activity_dir / "data"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df_letter = pd.read_csv(
        data_dir / "historical_requests_letter.csv.gz"
    ).drop_duplicates()
    df_letter["channel"] = "letter"

    df_web = pd.read_csv(
        data_dir / "historical_requests_web.csv.gz"
    ).drop_duplicates()
    df_web["channel"] = "web"

    df = pd.concat([df_letter, df_web], ignore_index=True)

    df["in_dt"] = pd.to_datetime(df["in_date"])
    df["out_dt"] = pd.to_datetime(df["out_date"])

    mask_answered = df["out_dt"].notna()
    df["calendar_days"] = np.nan
    df.loc[mask_answered, "calendar_days"] = (
        df.loc[mask_answered, "out_dt"] - df.loc[mask_answered, "in_dt"]
    ).dt.days

    in_dates = df.loc[mask_answered, "in_dt"].values.astype(
        "datetime64[D]"
    ) + np.timedelta64(1, "D")
    out_dates = df.loc[mask_answered, "out_dt"].values.astype(
        "datetime64[D]"
    ) + np.timedelta64(1, "D")

    df["business_days"] = np.nan
    df.loc[mask_answered, "business_days"] = np.busday_count(in_dates, out_dates)

    df["on_time"] = False
    df.loc[mask_answered, "on_time"] = df.loc[mask_answered, "business_days"] <= 15

    # 1. channel_summary
    ch_rows = []
    for ch in ["letter", "web"]:
        sub = df[df["channel"] == ch]
        reqs = int(len(sub))
        ans = int(sub["out_dt"].notna().sum())
        pend = int(sub["out_dt"].isna().sum())
        med_b = float(sub.loc[sub["out_dt"].notna(), "business_days"].median())
        ot_rate = float(sub["on_time"].mean())
        ch_rows.append(
            {
                "channel": ch,
                "requests": reqs,
                "answered": ans,
                "pending": pend,
                "median_business_days": med_b,
                "on_time_rate": ot_rate,
            }
        )
    channel_summary = pd.DataFrame(ch_rows)

    # 2. yearly_summary
    df["year"] = df["in_dt"].dt.year
    yr_rows = []
    for yr in sorted(df["year"].unique()):
        for ch in ["letter", "web"]:
            sub = df[(df["year"] == yr) & (df["channel"] == ch)]
            reqs = int(len(sub))
            pend = int(sub["out_dt"].isna().sum())
            ot_rate = float(sub["on_time"].mean())
            yr_rows.append(
                {
                    "year": int(yr),
                    "channel": ch,
                    "requests": reqs,
                    "pending": pend,
                    "on_time_rate": ot_rate,
                }
            )
    yearly_summary = pd.DataFrame(yr_rows)

    # 3. entry_day_summary
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    day_rows = []
    for d in day_order:
        sub = df[df["day_name"] == d]
        reqs = int(len(sub))
        med_c = float(sub.loc[sub["out_dt"].notna(), "calendar_days"].median())
        med_b = float(sub.loc[sub["out_dt"].notna(), "business_days"].median())
        day_rows.append(
            {
                "day_name": d,
                "requests": reqs,
                "median_calendar_days": med_c,
                "median_business_days": med_b,
            }
        )
    entry_day_summary = pd.DataFrame(day_rows)

    channel_summary.to_csv(submission_dir / "channel_summary.csv", index=False)
    yearly_summary.to_csv(submission_dir / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(
        submission_dir / "entry_day_summary.csv", index=False
    )

    return channel_summary, yearly_summary, entry_day_summary
