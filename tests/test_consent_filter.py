import pandas as pd

from vman_dq.dqa import _run_dqa_single, compute_aid, compute_ici, compute_ics, compute_rrs


def test_all_indicators_only_include_explicitly_consented_records():
    df = pd.DataFrame(
        {
            "id10013": ["yes", "no"],
            "id10008": ["spouse", "spouse"],
            "id10009": ["yes", "yes"],
            "id10023": ["2026-01-01", "2026-01-01"],
            "id10012": ["2026-01-02", "2026-01-02"],
            "id10064": ["yes", "yes"],
            "id10011": ["2026-01-01T10:00:00"] * 2,
            "id10481": ["2026-01-01T10:30:00"] * 2,
            "id10120": [5, 5],
            "id10147": ["no", "yes"],
            "id10148": [0, 6],
        }
    )

    ics = compute_ics(df)
    rrs = compute_rrs(df)
    ici, flags, _ = compute_ici(df)
    mid = compute_aid(df)

    for scores in (ics, rrs, ici, mid):
        assert pd.notna(scores.iloc[0])
        assert pd.isna(scores.iloc[1])
    assert pd.isna(flags.loc[1, "C6"])

    results = _run_dqa_single(df)
    for indicator in ("ics", "rrs", "ici", "aid"):
        assert results[indicator]["summary"]["n"] == 1
    assert results["ici"]["rule_violations"]["C6"] == {
        "description": "Fever duration exceeds total illness duration",
        "n": 0,
        "pct": 0.0,
    }
    assert results["ici"]["records_passing_all_rules"] == {"n": 1, "pct": 100.0}
    assert results["ici"]["mean_errors_per_record"] == 0.0
