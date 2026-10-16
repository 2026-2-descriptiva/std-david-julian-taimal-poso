import plotly.express as px
import streamlit as st

try:
    from .main import (
        DATA_FILE,
        calculate_kpis,
        filter_campaign_data,
        load_campaign_data,
        summarize_by_campaign,
        summarize_by_day,
        summarize_by_source,
    )
except ImportError:  # Permite ejecutar `streamlit run src/app.py`.
    from main import (
        DATA_FILE,
        calculate_kpis,
        filter_campaign_data,
        load_campaign_data,
        summarize_by_campaign,
        summarize_by_day,
        summarize_by_source,
    )


@st.cache_data
def get_campaign_data():
    """Cache the supplied classroom dataset during a dashboard session."""
    return load_campaign_data(DATA_FILE)


def format_currency(value):
    """Format a currency metric while preserving an unavailable ratio."""
    return "No disponible" if value is None else f"USD {value:,.2f}"


def main():
    """Render the filtered marketing dashboard."""
    st.set_page_config(page_title="Desempeño de campañas", layout="wide")
    st.title("Desempeño de campañas de marketing")
    st.caption("Datos suministrados para el taller; no representan resultados operativos reales.")

    data = get_campaign_data()
    minimum_date = data["utc_date"].min().date()
    maximum_date = data["utc_date"].max().date()

    with st.sidebar:
        st.header("Filtros")
        selected_dates = st.date_input(
            "Período",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
        )
        selected_sources = st.multiselect(
            "Fuente de tráfico",
            options=sorted(data["traffic_source"].unique()),
            default=sorted(data["traffic_source"].unique()),
        )
        selected_countries = st.multiselect(
            "País",
            options=sorted(data["country"].unique()),
            default=sorted(data["country"].unique()),
        )

    if len(selected_dates) != 2:
        st.info("Seleccione una fecha inicial y una fecha final.")
        st.stop()

    filtered_data = filter_campaign_data(
        data,
        start_date=selected_dates[0],
        end_date=selected_dates[1],
        traffic_sources=selected_sources,
        countries=selected_countries,
    )
    if filtered_data.empty:
        st.warning("Los filtros seleccionados no contienen campañas.")
        st.stop()

    kpis = calculate_kpis(filtered_data)
    metric_columns = st.columns(5)
    metric_columns[0].metric("Utilidad bruta", format_currency(kpis["gross_profit"]))
    metric_columns[1].metric("Ingreso", format_currency(kpis["revenue"]))
    metric_columns[2].metric("Inversión", format_currency(kpis["ad_spend"]))
    metric_columns[3].metric(
        "ROAS", "No disponible" if kpis["roas"] is None else f"{kpis['roas']:.2f}"
    )
    metric_columns[4].metric("CPC", format_currency(kpis["cpc"]))

    daily_summary = summarize_by_day(filtered_data)
    daily_figure = px.line(
        daily_summary,
        x="utc_date",
        y="gross_profit",
        title="Utilidad bruta diaria",
        labels={"utc_date": "Fecha", "gross_profit": "Utilidad bruta (USD)"},
        markers=True,
        color_discrete_sequence=["#4e79a7"],
    )
    st.plotly_chart(daily_figure)

    source_summary = summarize_by_source(filtered_data)
    source_figure = px.bar(
        source_summary.sort_values("gross_profit"),
        x="gross_profit",
        y="traffic_source",
        orientation="h",
        title="Utilidad bruta por fuente de tráfico",
        labels={"gross_profit": "Utilidad bruta (USD)", "traffic_source": "Fuente"},
        color_discrete_sequence=["#f28e2b"],
    )
    st.plotly_chart(source_figure)

    campaign_summary = summarize_by_campaign(filtered_data)
    st.subheader("Detalle por campaña")
    st.dataframe(campaign_summary, width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
    
    