from pathlib import Path


def test_01():
    assert Path("submission/campaign_summary.csv").is_file()
    assert Path("submission/daily_summary.csv").is_file()
    assert Path("submission/kpis.csv").is_file()
    assert Path("submission/source_summary.csv").is_file()
