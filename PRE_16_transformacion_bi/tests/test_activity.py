from pathlib import Path


def test_01():
    assert Path("submission/sales_analytics.csv").is_file()
