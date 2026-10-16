from pathlib import Path

import pandas as pd


PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_FOLDER / "data" / "campaign_data.csv"
SUBMISSION_FOLDER = PROJECT_FOLDER / "submission"

REQUIRED_COLUMNS = {
    "utc_date",
    "traffic_source",
    "country",
    "template_name",
    "impressions",
    "paid_clicks",
    "revenue",
    "ad_spend",
}
NUMERIC_COLUMNS = ("impressions", "paid_clicks", "revenue", "ad_spend")


def load_campaign_data(input_file=DATA_FILE):
    """Load the campaign data and derive profit from revenue and advertising spend."""
    data = pd.read_csv(input_file)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        missing_columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Faltan columnas requeridas: {missing_columns}.")

    data["utc_date"] = pd.to_datetime(data["utc_date"], errors="raise")
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="raise")

    if (data[list(NUMERIC_COLUMNS)] < 0).any().any():
        raise ValueError("Las métricas de campaña no pueden ser negativas.")

    data["gross_profit"] = data["revenue"] - data["ad_spend"]
    return data


def filter_campaign_data(data, start_date, end_date, traffic_sources=None, countries=None):
    """Return the campaign rows included by the dashboard filters."""
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    if start_date > end_date:
        raise ValueError("La fecha inicial no puede ser posterior a la fecha final.")

    filtered_data = data.loc[data["utc_date"].between(start_date, end_date)].copy()

    if traffic_sources is not None:
        filtered_data = filtered_data.loc[
            filtered_data["traffic_source"].isin(traffic_sources)
        ].copy()
    if countries is not None:
        filtered_data = filtered_data.loc[filtered_data["country"].isin(countries)].copy()

    return filtered_data


def safe_divide(numerator, denominator):
    """Return a ratio or None when its denominator is zero."""
    if denominator == 0:
        return None
    return numerator / denominator


def calculate_kpis(data):
    """Calculate additive campaign measures and ratios at the active filter scope."""
    impressions = int(data["impressions"].sum())
    paid_clicks = int(data["paid_clicks"].sum())
    revenue = float(data["revenue"].sum())
    ad_spend = float(data["ad_spend"].sum())
    gross_profit = revenue - ad_spend

    return {
        "impressions": impressions,
        "paid_clicks": paid_clicks,
        "revenue": revenue,
        "ad_spend": ad_spend,
        "gross_profit": gross_profit,
        "roas": safe_divide(revenue, ad_spend),
        "cpc": safe_divide(ad_spend, paid_clicks),
    }


def summarize_by_day(data):
    """Aggregate daily financial performance for the temporal chart."""
    return (
        data.groupby("utc_date", as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            ad_spend=("ad_spend", "sum"),
            gross_profit=("gross_profit", "sum"),
        )
        .sort_values("utc_date")
    )


def summarize_by_source(data):
    """Aggregate performance by traffic source and recompute source-level ratios."""
    source_summary = (
        data.groupby("traffic_source", as_index=False)
        .agg(
            impressions=("impressions", "sum"),
            paid_clicks=("paid_clicks", "sum"),
            revenue=("revenue", "sum"),
            ad_spend=("ad_spend", "sum"),
            gross_profit=("gross_profit", "sum"),
        )
        .sort_values("gross_profit", ascending=False)
    )
    source_summary["roas"] = source_summary.apply(
        lambda row: safe_divide(row["revenue"], row["ad_spend"]), axis=1
    )
    source_summary["cpc"] = source_summary.apply(
        lambda row: safe_divide(row["ad_spend"], row["paid_clicks"]), axis=1
    )
    return source_summary


def summarize_by_campaign(data):
    """Rank campaign templates by gross profit for operational detail."""
    return (
        data.groupby("template_name", as_index=False)
        .agg(
            impressions=("impressions", "sum"),
            paid_clicks=("paid_clicks", "sum"),
            revenue=("revenue", "sum"),
            ad_spend=("ad_spend", "sum"),
            gross_profit=("gross_profit", "sum"),
        )
        .sort_values("gross_profit", ascending=False)
    )


def export_dashboard_tables(output_folder=SUBMISSION_FOLDER):
    """Save the dashboard tables for the full campaign period."""
    data = load_campaign_data()
    pd.DataFrame([calculate_kpis(data)]).to_csv(output_folder / "kpis.csv", index=False)
    summarize_by_day(data).to_csv(output_folder / "daily_summary.csv", index=False)
    summarize_by_source(data).to_csv(output_folder / "source_summary.csv", index=False)
    summarize_by_campaign(data).to_csv(
        output_folder / "campaign_summary.csv", index=False
    )


if __name__ == "__main__":
    export_dashboard_tables()




