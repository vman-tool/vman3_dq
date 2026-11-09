import pandas as pd

from vman_dq.dqa import compute_rrs
from vman_dq.report import dqa_report


def test_rrs_literacy_and_education_weights():
    df = pd.DataFrame(
        {
            "id10013": ["yes"] * 8,
            "id10008": ["spouse"] * 8,
            "id10009": ["yes"] * 8,
            "id10023": ["2020-01-01"] * 8,
            "id10012": ["2020-01-02"] * 8,
            "id10064": ["yes", "no", "DK", "Ref", None, None, None, None],
            "id10063": [
                "no_formal_education",
                "higher_than_secondary_school",
                "DK",
                "Ref",
                None,
                "no_formal_education",
                "primary_school",
                "unrecognized",
            ],
        }
    )

    scores = compute_rrs(df)

    assert scores.tolist() == [100.0, 95.0, 90.0, 90.0, 90.0, 95.0, 100.0, 90.0]


def test_rrs_report_documents_literacy_and_education_weights():
    report = dqa_report({"sample": pd.DataFrame()})

    assert "literacy `yes` = 10 and `no` = 5" in report
    assert "`no_formal_education` = 5" in report
    assert "`primary_school`, `secondary_school`" in report
    assert "recognized value (including `DK`, `Ref`, missing, or unrecognized" in report
    assert "the component score is 0." in report
