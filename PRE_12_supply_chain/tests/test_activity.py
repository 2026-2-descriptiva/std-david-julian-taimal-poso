from pathlib import Path


def test_01():
    assert Path("submission/country_mode_summary.csv").is_file()
    assert Path("submission/country_summary.csv").is_file()
    assert Path("submission/freight_by_mode.csv").is_file()
    assert Path("submission/mode_summary.csv").is_file()
    assert Path("submission/monthly_summary.csv").is_file()
    assert Path("submission/overall_kpis.csv").is_file()
    assert Path("submission/priority_countries.csv").is_file()
    assert Path("submission/priority_segments.csv").is_file()
