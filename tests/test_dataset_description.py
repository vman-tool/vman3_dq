import pandas as pd

from vman_dq.report import dqa_report


def test_dataset_description_uses_consent_and_identifies_unavailable_metadata():
    df = pd.DataFrame(
        {
            "id10013": ["yes", "no", None],
            "id10019": ["female", "male", None],
            "isAdult": [1, 1, None],
            "isChild": [0, 0, None],
            "isNeonatal": [0, 0, None],
            "SubmitterID": ["account-1", "account-2", "account-1"],
            "FormVersion": ["v1", "v1", "v2"],
            "Status": [None, None, None],
            "SubmissionDate": [
                "2026-01-01T10:00:00Z",
                "2026-01-02T10:00:00Z",
                None,
            ],
        }
    )

    report = dqa_report({"sample": df})

    assert "### Table 9. Dataset characteristics" in report
    assert "| sample | 3 | Yes 1; No 1; Missing 1; Other/unknown 0 |" in report
    assert "Adult 1 (100.0%)" in report
    assert "Female 1 (100.0%); Male 0 (0.0%)" in report
    assert "| 2 | v1 (2), v2 (1) | 2026-01-01 to 2026-01-02 | Not recorded |" in report
    assert "completion status cannot be confirmed" in report
    assert "not a verified interviewer count" in report


def test_table_3_is_concise_and_table_9_contains_profile_details():
    df = pd.DataFrame(
        {
            "id10013": ["yes", "no", "yes"],
            "id10019": ["female", "male", None],
            "isadult": [1, 0, 0],
            "ischild": [0, 1, 0],
            "isneonate": [0, 0, 1],
            "id10011": [
                "2026-01-02T10:00:00Z",
                "2026-01-01T10:00:00Z",
                "bad timestamp",
            ],
            "id10481": [
                "2026-01-02T10:30:00Z",
                "2026-01-01T10:30:00Z",
                "2026-01-03T10:30:00Z",
            ],
        }
    )

    report = dqa_report(
        {"sample": df},
        meta={"sample": {"country": "Test", "who_va_version": "2022"}},
    )

    assert "| Dataset | Country | WHO-VA version | N | Consent | MID computable | RRS computable |" in report
    assert "| sample | Test | 2022 | 3 | 2 | Yes | No |" in report
    table3 = report.split("### Table 4.")[0]
    assert "Female" not in table3 and "Adult" not in table3
    assert "Timestamp coverage" not in table3
    assert "| Dataset | Records | Consent status | Age group among consented | Sex among consented | Timestamp coverage among consented" in report
    assert "Female 1 (50.0%); Male 0 (0.0%); Unknown 1 (50.0%)" in report
    assert "Adult 1 (50.0%)" in report
    assert "1 paired; 2026-01-02 to 2026-01-02" in report
    assert "`isAdult`, `isChild`, and `isNeonate`" in report
