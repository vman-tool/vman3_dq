# VMan3 DQA Indicator Report

Indicators: Informative Completeness Score (ICS), Respondent Reliability Score (RRS), Internal Consistency Index (ICI), Average Interview Duration (AID). Definitions follow *Four Practical Indicators for Real-Time Verbal Autopsy Data Quality Assessment* (Lyatuu et al.); ICI's C1 and C6-C9 follow that manuscript's methods section 2.3.3, extended with C2-C5 (age-group- and sex-restricted questions answered outside their WHO xForm-defined group, using field lists hand-verified against the WHO 2016/2022 xForms' variable-mapping sheet). The rule count (N) is open-ended and reflects only the rules computable for each dataset.

### Table 3. Dataset characteristics

| Dataset | Country | WHO-VA version | N | AID computable | RRS computable |
|---|---|---|---|---|---|
| va_2016_tz | - | - | 4344 | Yes | Yes |
| va_2022_es | - | - | 380 | Yes | Yes |
| va_2022_ng | - | - | 5474 | No | No |

### Table 4. ICS results by dataset

| Dataset | N | Mean (%) | Median (%) | SD | Min (%) | 5th pct (%) | 95th pct (%) |
|---|---|---|---|---|---|---|---|
| va_2016_tz | 4344 | 97.4 | 100.0 | 7.6 | 13.4 | 88.6 | 100.0 |
| va_2022_es | 380 | 96.4 | 98.8 | 6.6 | 25.0 | 86.4 | 100.0 |
| va_2022_ng | 5474 | 99.8 | 100.0 | 0.5 | 88.9 | 98.8 | 100.0 |

### Table 5 & 6. Respondent Reliability Score (RRS)

### Table 5. RRS continuous summary by dataset

| Dataset | N (eligible) | Mean | Median | SD | Min | Max |
|---|---|---|---|---|---|---|
| va_2016_tz | 3861 | 84.1 | 80.0 | 13.8 | 30.0 | 100.0 |
| va_2022_es | 349 | 81.8 | 87.0 | 12.8 | 35.0 | 100.0 |
| va_2022_ng | 0 | - | - | - | - | - |

### Table 6. RRS tier distribution by dataset

| Dataset | High (>= 80) | Moderate (50-79) | Low (< 50) |
|---|---|---|---|
| va_2016_tz | 67.1% | 32.2% | 0.6% |
| va_2022_es | 63.3% | 35.0% | 1.7% |
| va_2022_ng | - | - | - |

### Table 7. ICI results and rule-level violation counts

| Rule | Description | va_2016_tz (n=4344) | va_2022_es (n=380) | va_2022_ng (n=5474) |
|---|---|---|---|---|
| C1 | Interview date precedes death date (temporal impossibility) | 152 (3.5%) | 0 (0.0%) | n/a (field absent) |
| C2 | Adult-only question answered for a child or neonate | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| C3 | Child-only question answered for an adult or neonate | 9 (0.2%) | 0 (0.0%) | 0 (0.0%) |
| C4 | Neonate-only question answered for an adult or child | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| C5 | Female-only (pregnancy/maternal) question answered for a male decedent | 0 (0.0%) | 0 (0.0%) | 1 (0.0%) |
| C6 | Fever duration exceeds total illness duration | 42 (1.0%) | 4 (1.1%) | 115 (2.1%) |
| C7 | Cough duration exceeds total illness duration | 71 (1.6%) | 23 (6.1%) | 10 (0.2%) |
| C8 | Diarrhoea duration exceeds total illness duration | 15 (0.3%) | 7 (1.8%) | n/a (field absent) |
| C9 | Breathlessness duration exceeds total illness duration | 27 (0.6%) | 8 (2.1%) | 12 (0.2%) |
| Records passing all applied rules |  | 93.2% | 91.8% | 97.7% |
| Mean errors per record |  | 0.073 | 0.111 | 0.025 |

### Table 8. AID results by dataset

| Dataset | N (valid) | Mean (min) | Median (min) | SD | 5th pct (min) | 95th pct (min) |
|---|---|---|---|---|---|---|
| va_2016_tz | 2678 | 63.1 | 33.3 | 81.2 | 12.8 | 247.9 |
| va_2022_es | 281 | 56.9 | 27.3 | 79.1 | 11.7 | 235.1 |
| va_2022_ng | 0 | - | - | - | - | - |
