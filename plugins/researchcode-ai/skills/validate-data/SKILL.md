---
name: validate-data
description: Check datasets, definitions and calculations for research integrity
---

# Validate Data

## Data quality gate
1. Inspect schema, population, grain (firm, firm-year, CAM, KAM), units, currencies, time window and source licenses.
2. Validate duplicates, primary keys, missingness, attrition, merges, impossible values, outliers and temporal leakage. Never silently impute.
3. Independently recalculate main transformations with inspectable code and compare against source totals.
4. Explicitly document join cardinality, panel imbalance, industry exclusions, and restatements; distinguish sample errors from design choices.
5. Output data-quality report with failed thresholds, source evidence, consequences, fixes and reproducibility steps. Do not invent test statistics or sample counts.
