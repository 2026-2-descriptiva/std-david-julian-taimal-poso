from pathlib import Path


def test_01():
    assert Path("submission/monthly_region_sales.csv").is_file()
    assert Path("submission/north_category_sales.csv").is_file()
    assert Path("submission/north_product_drilldown.csv").is_file()
