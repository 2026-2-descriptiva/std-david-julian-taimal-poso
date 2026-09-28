from pathlib import Path


def test_01():
    assert Path("submission/bi_serving.db").is_file()
    assert Path("submission/dashboard_sales.csv").is_file()
    assert Path("submission/serving_manifest.csv").is_file()
