from pathlib import Path
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.
    """
    activity_dir = Path(__file__).resolve().parents[1]
    data_path = activity_dir / "data" / "superstore_orders.csv.gz"
    submission_dir = activity_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path, sep=";", decimal=",")

    # 1. profitability_summary
    lines = len(df)
    orders = int(df["Order ID"].nunique())
    sales = float(df["Sales"].sum())
    profit = float(df["Profit"].sum())
    profit_margin = profit / sales
    loss_lines = int((df["Profit"] < 0).sum())
    loss_line_rate = loss_lines / lines
    lost_profit = float(-df[df["Profit"] < 0]["Profit"].sum())

    summary = pd.DataFrame(
        [
            {
                "lines": lines,
                "orders": orders,
                "sales": sales,
                "profit": profit,
                "profit_margin": profit_margin,
                "loss_lines": loss_lines,
                "loss_line_rate": loss_line_rate,
                "lost_profit": lost_profit,
            }
        ]
    )

    # 2. discount_summary
    def get_band(d):
        if d == 0:
            return "0%"
        elif d <= 0.05:
            return "1%-5%"
        elif d <= 0.10:
            return "6%-10%"
        else:
            return "más de 10%"

    df["discount_band"] = df["Discount"].apply(get_band)
    band_order = ["0%", "1%-5%", "6%-10%", "más de 10%"]
    disc_rows = []
    for band in band_order:
        sub = df[df["discount_band"] == band]
        b_lines = len(sub)
        b_sales = float(sub["Sales"].sum())
        b_profit = float(sub["Profit"].sum())
        b_margin = b_profit / b_sales if b_sales else 0.0
        b_loss_rate = float((sub["Profit"] < 0).mean()) if b_lines else 0.0
        b_lost_profit = (
            float(-sub[sub["Profit"] < 0]["Profit"].sum())
            if (sub["Profit"] < 0).any()
            else 0.0
        )
        disc_rows.append(
            {
                "discount_band": band,
                "lines": b_lines,
                "sales": b_sales,
                "profit": b_profit,
                "profit_margin": b_margin,
                "loss_line_rate": b_loss_rate,
                "lost_profit": b_lost_profit,
            }
        )
    discounts = pd.DataFrame(disc_rows)

    # 3. priority_segments
    seg_rows = []
    for (seg, cat), sub in df.groupby(["Customer Segment", "Product Category"]):
        s_lines = len(sub)
        if s_lines >= 100:
            s_sales = float(sub["Sales"].sum())
            s_profit = float(sub["Profit"].sum())
            s_margin = s_profit / s_sales if s_sales else 0.0
            s_lost_profit = (
                float(-sub[sub["Profit"] < 0]["Profit"].sum())
                if (sub["Profit"] < 0).any()
                else 0.0
            )
            seg_rows.append(
                {
                    "Customer Segment": seg,
                    "Product Category": cat,
                    "lines": s_lines,
                    "sales": s_sales,
                    "profit": s_profit,
                    "profit_margin": s_margin,
                    "lost_profit": s_lost_profit,
                }
            )
    segments = (
        pd.DataFrame(seg_rows)
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    summary.to_csv(submission_dir / "profitability_summary.csv", index=False)
    discounts.to_csv(submission_dir / "discount_summary.csv", index=False)
    segments.to_csv(submission_dir / "priority_segments.csv", index=False)

    return summary, discounts, segments
