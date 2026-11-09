import pandas as pd

from vman_dq.report import dqa_report


def test_table_8_names_mid_and_defines_valid_duration_count():
    df = pd.DataFrame(
        {
            "id10013": ["no", "yes", "yes"],
            "id10011": [
                "2026-01-01T10:00:00",
                "2026-01-01T10:00:00",
                "2026-01-01T10:00:00",
            ],
            "id10481": [
                "2026-01-01T10:30:00",
                "2026-01-01T10:30:00",
                "2026-01-01T20:00:00",
            ],
        }
    )

    report = dqa_report({"sample": df})

    assert "### Table 8. MID results by dataset" in report
    assert "| sample | 2 | 1 | 30.0 | 30.0 | 0.0 | 30.0 | 30.0 |" in report
    assert "Consented counts records with `id10013` = `yes`." in report
    assert "N (valid) and all duration summaries use this subset." in report
