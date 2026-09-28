from pathlib import Path


def test_01():
    assert Path("submission/kpi_catalog.csv").is_file()
    assert Path("submission/kpi_publication_decision.csv").is_file()
    assert Path("submission/kpi_quality_report.csv").is_file()
    assert Path("submission/metric_lineage.csv").is_file()
