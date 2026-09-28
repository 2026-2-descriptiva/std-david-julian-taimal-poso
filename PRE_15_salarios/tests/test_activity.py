from pathlib import Path


def test_01():
    assert Path("submission/analysis_conclusions.csv").is_file()
    assert Path("submission/compensation_recommendations.csv").is_file()
    assert Path("submission/department_pay_gap.csv").is_file()
    assert Path("submission/high_salary_by_career.csv").is_file()
