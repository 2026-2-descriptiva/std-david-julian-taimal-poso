from pathlib import Path


def test_01():
    assert Path("submission/category_summary.csv").is_file()
    assert Path("submission/day_type_summary.csv").is_file()
    assert Path("submission/kpi_summary.csv").is_file()
    assert Path("submission/monthly_sales.csv").is_file()
    assert Path("submission/payment_summary.csv").is_file()
    assert Path("submission/priority_segments.csv").is_file()
    assert Path("submission/return_risk.csv").is_file()
    assert Path("submission/top_customers.csv").is_file()
    assert Path("submission/top_products.csv").is_file()
