import pandas as pd

from vman_dq.report import dqa_report


def test_table_7_reports_mean_ici_and_defines_summary_rows():
    df = pd.DataFrame(
        {
            "id10013": ["yes", "yes"],
            "id10120": [5, 5],
            "id10147": ["yes", "no"],
            "id10148": [6, 0],
            "id10153": ["no", "no"],
            "id10154": [0, 0],
            "id10181": ["no", "no"],
            "id10182": [0, 0],
            "id10159": ["no", "no"],
            "id10161": [0, 0],
        }
    )

    report = dqa_report({"sample": df})

    assert "| Mean ICI (%) |  | 87.50% |" in report
    assert "sample (consented n=2; total n=2)" in report
    assert "| Records passing all applied rules |  | 1 (50.0%) |" in report
    assert "| Mean errors per record |  | 0.500 |" in report
    assert "ICI = 100 × (1 − that record's violations / number of applicable rules)" in report
    assert "zero-violation consented records / consented records × 100" in report
    assert "total rule violations / consented records" in report
