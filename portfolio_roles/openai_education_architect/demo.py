"""Synthetic higher-education AI adoption review; no production deployment."""
import json

def review_pilot(plan):
    gaps = []
    for key in ("institution_id", "use_case", "academic_owner", "technical_owner",
                "approved_data_scope", "privacy_assessment_id", "baseline_metric",
                "pilot_success_metric", "accessibility_plan", "human_review_owner"):
        if not plan.get(key):
            gaps.append("missing_" + key)
    if plan.get("personal_data_approved") is not True:
        gaps.append("personal_data_not_approved")
    if plan.get("evaluation_completed") is not True:
        gaps.append("evaluation_incomplete")
    if plan.get("production_deployment_requested") is True:
        gaps.append("production_requires_separate_approval")
    return {"institution_id": plan.get("institution_id"),
            "state": "READY_FOR_PILOT_REVIEW" if not gaps else "PILOT_BLOCKED",
            "issues": sorted(set(gaps))}

if __name__ == "__main__":
    example = {"institution_id": "SYNTH-UNIVERSITY", "use_case": "faculty course Q&A sandbox",
               "academic_owner": "faculty_lead", "technical_owner": "IT_lead",
               "approved_data_scope": "public materials", "privacy_assessment_id": "SIM-DPIA-01",
               "baseline_metric": "staff prep minutes", "pilot_success_metric": "supported answers percent",
               "accessibility_plan": "review WCAG needs", "human_review_owner": "course_lead",
               "personal_data_approved": True, "evaluation_completed": True,
               "production_deployment_requested": False}
    print(json.dumps(review_pilot(example), indent=2))
