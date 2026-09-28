from pathlib import Path


def test_01():
    assert Path("submission/sales_mart.db").is_file()
