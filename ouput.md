# VMan3 DQA Indicator Report

Indicators: Informative Completeness Score (ICS), Respondent Reliability Score (RRS), Internal Consistency Index (ICI), Median Interview Duration (MID). Definitions follow *Four Practical Indicators for Real-Time Verbal Autopsy Data Quality Assessment* (Lyatuu et al.). All indicators are computed only for records with explicit consent (`id10013` = `yes`); records with no, unknown, or missing consent have blank scores. ICI's C1 and C6-C9 follow that manuscript's methods section 2.3.3, extended with C2-C5 (age-group- and sex-restricted questions answered outside their WHO xForm-defined group, using field lists hand-verified against the WHO 2016/2022 xForms' variable-mapping sheet). The rule count (N) is open-ended and reflects only the rules computable for each dataset.

### Table 3. Dataset characteristics

| Dataset | Country | WHO-VA version | N | Consent | MID computable | RRS computable |
|---|---|---|---:|---:|---|---|
| va_2016_tz | - | - | 4,344 | 3,964 | Yes | Yes |
| va_2022_es | - | - | 380 | 373 | Yes | Yes |
| va_2022_ng | - | - | 5,474 | 5,473 | No | No |

### Table 4. ICS results by dataset

| Dataset | N | Mean (%) | Median (%) | SD | Min (%) | 5th pct (%) | 95th pct (%) |
|---|---|---|---|---|---|---|---|
| va_2016_tz | 3964 | 97.3 | 100.0 | 7.6 | 13.4 | 88.6 | 100.0 |
| va_2022_es | 373 | 96.6 | 98.8 | 5.6 | 55.4 | 86.6 | 100.0 |
| va_2022_ng | 5473 | 99.8 | 100.0 | 0.5 | 88.9 | 98.8 | 100.0 |

### Table 5 & 6. Respondent Reliability Score (RRS)

### Table 5. RRS continuous summary by dataset

Literacy/education component weights (maximum 10 points): literacy `yes` = 10 and `no` = 5; if literacy does not provide a score, `no_formal_education` = 5 and `primary_school`, `secondary_school`, or `higher_than_secondary_school` = 10. If neither field has a recognized value (including `DK`, `Ref`, missing, or unrecognized responses), the component score is 0.

| Dataset | N (eligible) | Mean | Median | SD | Min | Max |
|---|---|---|---|---|---|---|
| va_2016_tz | 3861 | 83.5 | 80.0 | 13.9 | 30.0 | 100.0 |
| va_2022_es | 349 | 79.4 | 80.0 | 13.5 | 35.0 | 100.0 |
| va_2022_ng | 0 | - | - | - | - | - |

### Table 6. RRS tier distribution by dataset

| Dataset | High (>= 80) | Moderate (50-79) | Low (< 50) |
|---|---|---|---|
| va_2016_tz | 67.1% | 32.0% | 0.9% |
| va_2022_es | 62.8% | 35.2% | 2.0% |
| va_2022_ng | - | - | - |

### Table 7. ICI results and rule-level violation counts

| Rule | Description | va_2016_tz (consented n=3964; total n=4344) | va_2022_es (consented n=373; total n=380) | va_2022_ng (consented n=5473; total n=5474) |
|---|---|---|---|---|
| C1 | Interview date precedes death date (temporal impossibility) | 152 (3.8%) | 0 (0.0%) | n/a (field absent) |
| C2 | Adult-only question answered for a child or neonate | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| C3 | Child-only question answered for an adult or neonate | 5 (0.1%) | 0 (0.0%) | 0 (0.0%) |
| C4 | Neonate-only question answered for an adult or child | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| C5 | Female-only (pregnancy/maternal) question answered for a male decedent | 0 (0.0%) | 0 (0.0%) | 1 (0.0%) |
| C6 | Fever duration exceeds total illness duration | 37 (0.9%) | 4 (1.1%) | 115 (2.1%) |
| C7 | Cough duration exceeds total illness duration | 65 (1.6%) | 23 (6.2%) | 10 (0.2%) |
| C8 | Diarrhoea duration exceeds total illness duration | 15 (0.4%) | 7 (1.9%) | n/a (field absent) |
| C9 | Breathlessness duration exceeds total illness duration | 27 (0.7%) | 8 (2.1%) | 12 (0.2%) |
| Mean ICI (%) |  | 99.16% | 98.75% | 99.64% |
| Records passing all applied rules |  | 3683 (92.9%) | 342 (91.7%) | 5347 (97.7%) |
| Mean errors per record |  | 0.076 | 0.113 | 0.025 |

Note: Mean ICI is the average per-record score, where each record's ICI = 100 × (1 − that record's violations / number of applicable rules). Rule-level percentages, records passing all applied rules (zero violations), and mean errors per record use consented records as the denominator. Records passing all rules = zero-violation consented records / consented records × 100. Mean errors per record = total rule violations / consented records. Rules whose required fields are absent are excluded from that dataset's applicable-rule count.

### Table 8. MID results by dataset

| Dataset | Consented | N (valid) | Mean (min) | Median (min) | SD | 5th pct (min) | 95th pct (min) |
|---|---:|---:|---:|---:|---:|---:|---:|
| va_2016_tz | 3964 | 2678 | 63.1 | 33.3 | 81.2 | 12.8 | 247.9 |
| va_2022_es | 373 | 281 | 56.9 | 27.3 | 79.1 | 11.7 | 235.1 |
| va_2022_ng | 5473 | 0 | - | - | - | - | - |

Note: Consented counts records with `id10013` = `yes`. MID is median interview duration, calculated among consented records with parseable interview start (`id10011`) and end (`id10481`) times whose duration is greater than 0 and less than 480 minutes. N (valid) and all duration summaries use this subset.

### Table 9. Dataset characteristics

| Dataset | Records | Consent status | Age group among consented | Sex among consented | Timestamp coverage among consented (`id10011` + `id10481`) | Completion/submission metadata | Submitter accounts* | Form version evidence | Submission date range | Export date |
|---|---:|---|---|---|---|---|---:|---|---|---|
| va_2016_tz | 4,344 | Yes 3,964; No 34; Missing 346; Other/unknown 0 | Adult 3,572 (90.1%); Child 323 (8.1%); Neonatal 69 (1.7%); Unclassified 0 (0.0%) | Female 1,650 (41.6%); Male 2,314 (58.4%); Unknown 0 (0.0%) | 3,964 paired; 2015-01-01 to 2026-07-30 | Status blank 4,344/4,344; SubmissionDate present 4,344/4,344; completion status not explicitly available | 2 | 20220521 (63), 20220712 (283), 20230413 (2,031), 20250228 (30), 20250306 (1), 20250307 (1,936) | 2022-05-24 to 2026-08-01 | Not recorded |
| va_2022_es | 380 | Yes 373; No 7; Missing 0; Other/unknown 0 | Adult 364 (97.6%); Child 9 (2.4%); Neonatal 0 (0.0%); Unclassified 0 (0.0%) | Female 175 (46.9%); Male 198 (53.1%); Unknown 0 (0.0%) | 373 paired; 2026-01-14 to 2026-04-11 | Status blank 380/380; SubmissionDate present 380/380; completion status not explicitly available | 36 | 2023072701 (8), 2023072701_1 (372) | 2026-01-14 to 2026-04-15 | Not recorded |
| va_2022_ng | 5,474 | Yes 5,473; No 1; Missing 0; Other/unknown 0 | Adult 1,155 (21.1%); Child 3,654 (66.8%); Neonatal 664 (12.1%); Unclassified 0 (0.0%) | Female 3,079 (56.3%); Male 2,394 (43.7%); Unknown 0 (0.0%) | Timestamp fields absent | Status field absent; SubmissionDate absent; completion status not explicitly available | Unavailable | FormVersion absent; customization details unavailable | SubmissionDate absent | Not recorded |

Notes: Consent is `id10013` (`yes`/`no`); age groups use the WHO-VA `isAdult`, `isChild`, and `isNeonate` flags (case-insensitive; exports may name the neonatal flag `isNeonatal`); sex uses `id10019`. Age and sex distributions are among consented records. `SubmitterID` counts distinct submitting accounts and is only a proxy for interviewers, not a verified interviewer count. `Status` is blank or absent in these exports, so completion status cannot be confirmed; `SubmissionDate` describes record submission dates, not the export date. `FormVersion` values show version evidence, but do not describe the customizations themselves. The bundled dictionary contains only field type, name, and relevance and does not define these metadata fields or the consent/sex/age variables. Timestamp coverage counts consented records with both `id10011` and `id10481` parseable; the date span is earliest start to latest end.
