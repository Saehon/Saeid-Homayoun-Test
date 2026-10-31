# Third-party evaluation management — Frontier Assurance role

## Goal

Demonstrate independent assessment coordination: evaluators own the labels and test scope, developers cannot edit holdout gold, results expose uncertainty and abstention, and critical findings require human escalation. **This is a research sample, not an actual frontier model assessment or employer-endorsed assurance mechanism.**

## Proposed gates

1. Charter and scope: model/safeguard version, decision context, assessed capability, stakeholder and risk-owner sign-off.
2. Independence: conflict-of-interest review, evaluator contracting, limited access and separation of model builders from gold labels.
3. Protocol: pre-register metrics, evidence admissibility, stratified risk levels, abstention rules and external challenge conditions.
4. Leakage: forbid overlap of development and blind evaluation IDs; preserve hashes and version history.
5. Evidence: immutable evidence IDs and source references; ensure public disclosure summaries distinguish claims, measurements and uncertainties.
6. Escalation: unresolved critical findings block the release recommendation, with independent reviewer and accountable decision owner.
7. Post-review: examine residual risks and replications. Never infer frontier safety from a small or synthetic task set.

## Offline model comparison interface

```bash
python -m portfolio_roles.frontier_assurance.independent_eval_adapter --gold /private/independently_labelled.jsonl --pred model_A=/private/model_A.jsonl --pred model_B=/private/model_B.jsonl --dev-ids /private/development_ids.json --out /private/independent_review.json
```

Gold labels need case_id, gold_label (0/1), independent_labeler_id, label_protocol and evidence_id. Candidate files need case_id and predicted_label. **Schema does not verify evaluator's real independence.** Reviewers must confirm it off-platform. All files stay local; no secret test cases or unsafe prompt sets are distributed.
