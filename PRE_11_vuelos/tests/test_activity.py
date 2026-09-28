from pathlib import Path


def test_01():
    assert Path("submission/carrier_summary.csv").is_file()
    assert Path("submission/day_hour_delay.csv").is_file()
    assert Path("submission/monthly_national_kpis.csv").is_file()
    assert Path("submission/overall_kpis.csv").is_file()
    assert Path("submission/priority_segments.csv").is_file()
    assert Path("submission/seasonality.csv").is_file()
