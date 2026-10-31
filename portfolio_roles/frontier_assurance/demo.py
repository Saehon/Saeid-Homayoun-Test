"""Review an independent-evaluation record; not a model safety certification."""
import json

def review_evaluation(record):
    gaps = []
    for field in ("evaluation_id", "model_id", "protocol_version", "assessor",
                  "model_team", "public_method_url", "evidence_id"):
        if not record.get(field):
            gaps.append("missing_" + field)
    if record.get("assessor") and record.get("assessor") == record.get("model_team"):
        gaps.append("assessor_conflict")
    if record.get("holdout_declared") is not True:
        gaps.append("holdout_not_documented")
    total = record.get("planned_tests")
    performed = record.get("completed_tests")
    if (not isinstance(total, int) or isinstance(total, bool) or total <= 0 or
        not isinstance(performed, int) or isinstance(performed, bool) or performed < total):
        gaps.append("incomplete_or_invalid_coverage")
    if record.get("unresolved_critical_findings", 1) != 0:
        gaps.append("critical_findings_unresolved")
    return {"evaluation_id": record.get("evaluation_id"),
            "evidence_status": "READY_FOR_INDEPENDENT_REVIEW" if not gaps else "INSUFFICIENT_EVIDENCE",
            "gaps": sorted(set(gaps))}

if __name__ == "__main__":
    synthetic = {"evaluation_id": "DEMO-001", "model_id": "synthetic-model",
                 "protocol_version": "0.1", "assessor": "external_lab",
                 "model_team": "model_dev", "public_method_url": "https://example.org/method",
                 "evidence_id": "SYNTH-REPORT-01", "holdout_declared": True,
                 "planned_tests": 20, "completed_tests": 20, "unresolved_critical_findings": 0}
    print(json.dumps(review_evaluation(synthetic), indent=2))
