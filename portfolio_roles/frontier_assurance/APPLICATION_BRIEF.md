# Application-ready project summary — OpenAI — Research Program Manager, Frontier Assurance

**Authorship statement:** This `portfolio_roles/frontier_assurance` contribution is a new, independent, role-specific research demonstration. The host repository may contain third-party material; ownership of all pre-existing repository content is **not claimed**. Nothing here establishes employment, partnership or endorsement by the named employer.

## Challenge addressed

third-party assessment governance, independent evaluation, holdout leakage checks, scientific reproducibility.

## What has been developed and verified

- A Python standard-library demonstration with explicit decision states and negative tests.
- Ten synthetic contract cases: eight designed to be blocked, two ready for review.
- A comparison with a weak *always-ready* baseline, plus block-class precision/recall/F1, case-level reasoning and dataset SHA-256.
- GitHub Actions continuous integration with machine-readable JSON reports.
- Role-specific evaluation and scientific validation gates.

**Evidence level:** successfully executed synthetic regression/contract checks only. The gold labels were designed from the same rule specification, so the benchmark does not demonstrate out-of-sample predictive accuracy or a genuine AI model comparison.

## 90-second interview demo

Show a deliberately contaminated holdout being rejected and compare two candidate output files with abstentions.

## Suggested CV sentence (accurate only while CI remains green)

"Designed and implemented a reproducible, role-aligned Python evidence-evaluation prototype with fail-closed cases, test automation, structured quality metrics, and documented governance limitations."

## Next engineering/research milestone

Recruit external qualified evaluators and independently label held-out assessments; preserve conflict-of-interest documentation.

## Release / disclosure gates

| Gate | Current status |
|---|---|
| Code created and unit tested | PASS — GitHub Actions evidence |
| Synthetic contract benchmark | PASS — internally constructed cases |
| External or domain-licensed data | NOT YET VERIFIED |
| Real LLM or production-system evaluation | NOT RUN |
| Independent/blind expert code and data review | PENDING |
| Ethics, security, privacy and IP review where required | PENDING |
| Production assurance, compliance or deployment certification | NOT CLAIMED |

**Research investigator:** Saeid Homayoun · ORCID: https://orcid.org/0000-0002-2536-0446.
