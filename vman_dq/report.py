"""
Markdown report generator for the four DQA indicators (ICS, RRS, ICI, AID),
reproducing the table structure used in the source manuscript (Tables 3-8)
for an arbitrary set of datasets.

This module only formats results already computed by `vman_dq.dqa`; it has
no I/O of its own beyond returning a string, so it works identically
whether the input came from CSV files (local validation) or records
fetched from a database (production use).
"""

from typing import Dict, Optional

import pandas as pd

from .dqa import _consented_mask, _dedupe_columns, _dist_stats, _run_dqa_single

__all__ = ["dqa_report"]


def _fmt(v, decimals: int = 1) -> str:
    if v is None:
        return "-"
    return f"{v:.{decimals}f}"


def _fmt_pct_n(n: Optional[int], pct: Optional[float]) -> str:
    if n is None or pct is None:
        return "-"
    return f"{n} ({pct:.1f}%)"


def _table_3_overview(
    results: Dict[str, dict],
    meta: Dict[str, dict],
    dataframes: Dict[str, "pd.DataFrame"],
) -> str:
    lines = [
        "### Table 3. Dataset characteristics",
        "",
        "| Dataset | Country | WHO-VA version | N | Consent | MID computable | RRS computable |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for name, r in results.items():
        m = meta.get(name, {})
        df = _dedupe_columns(dataframes[name])
        n_consented = int(_consented_mask(df).sum())
        mid_ok = "Yes" if r["aid"]["computable"] else "No"
        rrs_ok = "Yes" if r["rrs"]["computable"] else "No"
        lines.append(
            f"| {name} | {m.get('country', '-')} | {m.get('who_va_version', '-')} | "
            f"{r['n_records']:,} | {n_consented:,} | {mid_ok} | {rrs_ok} |"
        )
    return "\n".join(lines)


def _table_4_ics(results: Dict[str, dict]) -> str:
    lines = [
        "### Table 4. ICS results by dataset",
        "",
        "| Dataset | N | Mean (%) | Median (%) | SD | Min (%) | 5th pct (%) | 95th pct (%) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, r in results.items():
        s = r["ics"]["summary"]
        lines.append(
            f"| {name} | {s['n']} | {_fmt(s['mean'])} | {_fmt(s['median'])} | "
            f"{_fmt(s['sd'])} | {_fmt(s['min'])} | {_fmt(s['p5'])} | {_fmt(s['p95'])} |"
        )
    return "\n".join(lines)


def _table_5_rrs_continuous(results: Dict[str, dict]) -> str:
    lines = [
        "### Table 5. RRS continuous summary by dataset",
        "",
        "Literacy/education component weights (maximum 10 points): literacy "
        "`yes` = 10 and `no` = 5; if literacy does not provide a score, "
        "`no_formal_education` = 5 and `primary_school`, `secondary_school`, "
        "or `higher_than_secondary_school` = 10. If neither field has a "
        "recognized value (including `DK`, `Ref`, missing, or unrecognized "
        "responses), the component score is 0.",
        "",
        "| Dataset | N (eligible) | Mean | Median | SD | Min | Max |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, r in results.items():
        s = r["rrs"]["summary"]
        if s["n"] == 0:
            lines.append(f"| {name} | 0 | - | - | - | - | - |")
            continue
        lines.append(
            f"| {name} | {s['n']} | {_fmt(s['mean'])} | {_fmt(s['median'])} | "
            f"{_fmt(s['sd'])} | {_fmt(s['min'])} | {_fmt(s['max'])} |"
        )
    return "\n".join(lines)


def _table_6_rrs_tiers(results: Dict[str, dict]) -> str:
    lines = [
        "### Table 6. RRS tier distribution by dataset",
        "",
        "| Dataset | High (>= 80) | Moderate (50-79) | Low (< 50) |",
        "|---|---|---|---|",
    ]
    for name, r in results.items():
        t = r["rrs"]["tiers"]
        if not t:
            lines.append(f"| {name} | - | - | - |")
            continue
        lines.append(
            f"| {name} | {t['High']['pct']:.1f}% | {t['Moderate']['pct']:.1f}% | {t['Low']['pct']:.1f}% |"
        )
    return "\n".join(lines)


def _table_7_ici(results: Dict[str, dict]) -> str:
    names = list(results.keys())
    all_rules = []
    for r in results.values():
        for rid in r["ici"]["rules_applied"]:
            if rid not in all_rules:
                all_rules.append(rid)
    all_rules.sort()

    header = "| Rule | Description | " + " | ".join(
        f"{n} (consented n={results[n]['n_consented']}; total n={results[n]['n_records']})"
        for n in names
    ) + " |"
    sep = "|---|---|" + "---|" * len(names)
    lines = ["### Table 7. ICI results and rule-level violation counts", "", header, sep]

    from .dqa import ICI_RULE_DESCRIPTIONS
    for rid in all_rules:
        desc = ICI_RULE_DESCRIPTIONS.get(rid, "")
        row = [rid, desc]
        for name in names:
            rv = results[name]["ici"]["rule_violations"].get(rid)
            if rv is None:
                row.append("n/a (field absent)")
            else:
                row.append(_fmt_pct_n(rv["n"], rv["pct"]))
        lines.append("| " + " | ".join(row) + " |")

    ici_row = ["Mean ICI (%)", ""]
    pass_row = ["Records passing all applied rules", ""]
    err_row = ["Mean errors per record", ""]
    for name in names:
        ici_mean = results[name]["ici"]["summary"]["mean"]
        pa = results[name]["ici"]["records_passing_all_rules"]
        me = results[name]["ici"]["mean_errors_per_record"]
        ici_row.append(f"{ici_mean:.2f}%" if ici_mean is not None else "-")
        pass_row.append(f"{pa['n']} ({pa['pct']:.1f}%)" if pa else "-")
        err_row.append(_fmt(me, 3) if me is not None else "-")
    lines.append("| " + " | ".join(ici_row) + " |")
    lines.append("| " + " | ".join(pass_row) + " |")
    lines.append("| " + " | ".join(err_row) + " |")
    lines.extend(
        [
            "",
            "Note: Mean ICI is the average per-record score, where each record's "
            "ICI = 100 × (1 − that record's violations / number of applicable "
            "rules). Rule-level percentages, records passing all applied rules "
            "(zero violations), and mean errors per record use consented records "
            "as the denominator. Records passing all rules = zero-violation "
            "consented records / consented records × 100. Mean errors per "
            "record = total rule violations / consented records. Rules whose "
            "required fields are absent are excluded from that dataset's "
            "applicable-rule count.",
        ]
    )
    return "\n".join(lines)


def _table_8_mid(results: Dict[str, dict], dataframes: Dict[str, "pd.DataFrame"]) -> str:
    lines = [
        "### Table 8. MID results by dataset",
        "",
        "| Dataset | Consented | N (valid) | Mean (min) | Median (min) | SD | 5th pct (min) | 95th pct (min) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, r in results.items():
        df = dataframes[name]
        consented = _consented_mask(df)
        n_consented = int(consented.sum())
        valid_mid = r["aid"]["per_record"].where(consented).dropna()
        s = _dist_stats(valid_mid)
        if s["n"] == 0:
            lines.append(f"| {name} | {n_consented} | 0 | - | - | - | - | - |")
            continue
        lines.append(
            f"| {name} | {n_consented} | {s['n']} | {_fmt(s['mean'])} | "
            f"{_fmt(s['median'])} | {_fmt(s['sd'])} | {_fmt(s['p5'])} | {_fmt(s['p95'])} |"
        )
    lines.extend(
        [
            "",
            "Note: Consented counts records with `id10013` = `yes`. MID is "
            "median interview duration, calculated among consented records "
            "with parseable interview start (`id10011`) and end (`id10481`) "
            "times whose duration is greater than 0 and less than 480 minutes. "
            "N (valid) and all duration summaries use this subset.",
        ]
    )
    return "\n".join(lines)


def _count_pct(count: int, denominator: int) -> str:
    if not denominator:
        return f"{count} (n/a)"
    return f"{count:,} ({count / denominator * 100:.1f}%)"


def _table_9_dataset_description(
    results: Dict[str, dict],
    dataframes: Dict[str, "pd.DataFrame"],
) -> str:
    lines = [
        "### Table 9. Dataset characteristics",
        "",
        "| Dataset | Records | Consent status | Age group among consented | Sex among consented | Timestamp coverage among consented (`id10011` + `id10481`) | Completion/submission metadata | Submitter accounts* | Form version evidence | Submission date range | Export date |",
        "|---|---:|---|---|---|---|---|---:|---|---|---|",
    ]

    for name, result in results.items():
        df = _dedupe_columns(dataframes[name])
        n_records = len(df)
        consent_col = next((c for c in df.columns if c.lower() == "id10013"), None)
        if consent_col is None:
            consent = pd.Series("unknown", index=df.index)
        else:
            consent = df[consent_col].astype("string").str.strip().str.lower()
            consent = consent.fillna("").replace("", "missing")
            consent = consent.where(
                consent.isin({"yes", "no", "missing"}), "other/unknown"
            )
        consented = consent.eq("yes")
        n_consented = int(consented.sum())
        consent_counts = consent.value_counts()
        consent_summary = "; ".join(
            f"{label} {int(consent_counts.get(value, 0)):,}"
            for value, label in (
                ("yes", "Yes"),
                ("no", "No"),
                ("missing", "Missing"),
                ("other/unknown", "Other/unknown"),
            )
        )

        age_flags = {}
        for label, field in (
            ("Adult", "isAdult"),
            ("Child", "isChild"),
            ("Neonatal", "isNeonatal"),
        ):
            col = next((c for c in df.columns if c.lower() == field.lower()), None)
            age_flags[label] = (
                pd.to_numeric(df[col], errors="coerce").eq(1)
                if col is not None
                else pd.Series(False, index=df.index)
            )
        age_flag_count = sum(age_flags.values())
        age_unknown = consented & age_flag_count.ne(1)
        age_parts = [
            f"{label} {_count_pct(int((consented & flag).sum()), n_consented)}"
            for label, flag in age_flags.items()
        ]
        age_parts.append(f"Unclassified {_count_pct(int(age_unknown.sum()), n_consented)}")

        sex_col = next((c for c in df.columns if c.lower() == "id10019"), None)
        if sex_col is None:
            sex = pd.Series("unknown", index=df.index)
        else:
            sex = df[sex_col].astype("string").str.strip().str.lower()
            sex = sex.fillna("").replace("", "unknown")
            sex = sex.where(sex.isin({"female", "male"}), "unknown")
        sex_parts = [
            f"{label} {_count_pct(int((consented & sex.eq(value)).sum()), n_consented)}"
            for value, label in (("female", "Female"), ("male", "Male"), ("unknown", "Unknown"))
        ]

        start_col = next((c for c in df.columns if c.lower() == "id10011"), None)
        end_col = next((c for c in df.columns if c.lower() == "id10481"), None)
        if start_col is None or end_col is None:
            timestamp_coverage = "Timestamp fields absent"
        else:
            start = pd.to_datetime(df[start_col], errors="coerce", utc=True)
            end = pd.to_datetime(df[end_col], errors="coerce", utc=True)
            paired = consented & start.notna() & end.notna()
            if paired.any():
                timestamp_coverage = (
                    f"{int(paired.sum()):,} paired; "
                    f"{start[paired].min().date()} to {end[paired].max().date()}"
                )
            else:
                timestamp_coverage = "0 paired; no parseable coverage"

        status_col = next((c for c in df.columns if c.lower() == "status"), None)
        submission_col = next(
            (c for c in df.columns if c.lower() == "submissiondate"), None
        )
        if status_col is None:
            status_note = "Status field absent"
        else:
            status_values = df[status_col].astype("string").str.strip()
            n_status = int((status_values.notna() & status_values.ne("")).sum())
            status_note = (
                f"Status populated {n_status:,}/{n_records:,}"
                if n_status
                else f"Status blank {n_records:,}/{n_records:,}"
            )
        if submission_col is not None:
            submission = df[submission_col].astype("string").str.strip()
            n_submitted = int((submission.notna() & submission.ne("")).sum())
            status_note += f"; SubmissionDate present {n_submitted:,}/{n_records:,}"
        else:
            status_note += "; SubmissionDate absent"
        status_note += "; completion status not explicitly available"

        submitter_col = next(
            (c for c in df.columns if c.lower() == "submitterid"), None
        )
        if submitter_col is None:
            submitter_count = "Unavailable"
        else:
            submitter = df[submitter_col].astype("string").str.strip()
            submitter_count = str(int(submitter[submitter.notna() & submitter.ne("")].nunique()))

        version_col = next(
            (c for c in df.columns if c.lower() == "formversion"), None
        )
        if version_col is None:
            version_note = "FormVersion absent; customization details unavailable"
        else:
            versions = df[version_col].astype("string").str.strip()
            version_counts = versions[versions.notna() & versions.ne("")].value_counts()
            version_note = (
                ", ".join(
                    f"{version} ({int(count):,})"
                    for version, count in sorted(version_counts.items())
                )
                if not version_counts.empty
                else "FormVersion blank; customization details unavailable"
            )

        if submission_col is None:
            submission_range = "SubmissionDate absent"
        else:
            submission_dates = pd.to_datetime(
                df[submission_col], errors="coerce", utc=True
            ).dropna()
            submission_range = (
                f"{submission_dates.min().date()} to {submission_dates.max().date()}"
                if not submission_dates.empty
                else "No parseable submission dates"
            )

        lines.append(
            f"| {name} | {n_records:,} | {consent_summary} | "
            f"{'; '.join(age_parts)} | {'; '.join(sex_parts)} | "
            f"{timestamp_coverage} | {status_note} | {submitter_count} | "
            f"{version_note} | {submission_range} | Not recorded |"
        )

    lines.extend(
        [
            "",
            "Notes: Consent is `id10013` (`yes`/`no`); age groups use the WHO-VA "
            "`isAdult`, `isChild`, and `isNeonate` flags (case-insensitive; "
            "exports may name the neonatal flag `isNeonatal`); sex uses "
            "`id10019`. Age and sex distributions are among consented records. "
            "`SubmitterID` "
            "counts distinct submitting accounts and is only a proxy for "
            "interviewers, not a verified interviewer count. `Status` is blank "
            "or absent in these exports, so completion status cannot be confirmed; "
            "`SubmissionDate` describes record submission dates, not the export "
            "date. `FormVersion` values show version evidence, but do not describe "
            "the customizations themselves. The bundled dictionary contains only "
            "field type, name, and relevance and does not define these metadata "
            "fields or the consent/sex/age variables. Timestamp coverage counts "
            "consented records with both `id10011` and `id10481` parseable; the "
            "date span is earliest start to latest end.",
        ]
    )
    return "\n".join(lines)


def dqa_report(
    dataframes: Dict[str, "pd.DataFrame"],
    meta: Optional[Dict[str, dict]] = None,
    title: str = "VMan3 DQA Indicator Report",
) -> str:
    """Compute all four indicators for each named DataFrame and render a
    Markdown report with indicator tables and a descriptive dataset profile.

    Parameters
    ----------
    dataframes: mapping of dataset label -> DataFrame of VA records
    meta: optional mapping of dataset label -> {"country": ..., "who_va_version": ...},
          used only to populate Table 3
    """
    meta = meta or {}
    results = {name: _run_dqa_single(df) for name, df in dataframes.items()}

    sections = [
        f"# {title}",
        "",
        "Indicators: Informative Completeness Score (ICS), Respondent Reliability "
        "Score (RRS), Internal Consistency Index (ICI), Median Interview Duration "
        "(MID). Definitions follow *Four Practical Indicators for Real-Time Verbal "
        "Autopsy Data Quality Assessment* (Lyatuu et al.). All indicators are "
        "computed only for records with explicit consent (`id10013` = `yes`); "
        "records with no, unknown, or missing consent have blank scores. "
        "ICI's C1 and C6-C9 follow that manuscript's methods section 2.3.3, "
        "extended with C2-C5 "
        "(age-group- and sex-restricted questions answered outside their WHO "
        "xForm-defined group, using field lists hand-verified against the WHO "
        "2016/2022 xForms' variable-mapping sheet). The rule count (N) is "
        "open-ended and reflects only the rules computable for each dataset.",
        "",
        _table_3_overview(results, meta, dataframes),
        "",
        _table_4_ics(results),
        "",
        "### Table 5 & 6. Respondent Reliability Score (RRS)",
        "",
        _table_5_rrs_continuous(results),
        "",
        _table_6_rrs_tiers(results),
        "",
        _table_7_ici(results),
        "",
        _table_8_mid(results, dataframes),
        "",
        _table_9_dataset_description(results, dataframes),
        "",
    ]
    return "\n".join(sections)