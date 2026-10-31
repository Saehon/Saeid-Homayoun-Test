import unittest
from portfolio_roles.openai_education_architect.demo import review_pilot

class TestEduArchitect(unittest.TestCase):
    def setUp(self):
        self.plan = {"institution_id": "U", "use_case": "sandbox", "academic_owner": "a",
                     "technical_owner": "t", "approved_data_scope": "public",
                     "privacy_assessment_id": "SYN-01", "baseline_metric": "time",
                     "pilot_success_metric": "quality", "accessibility_plan": "review",
                     "human_review_owner": "h", "personal_data_approved": True,
                     "evaluation_completed": True, "production_deployment_requested": False}
    def test_synthetic_pilot_ready_for_review(self):
        self.assertEqual(review_pilot(self.plan)["state"], "READY_FOR_PILOT_REVIEW")
    def test_data_without_approval_blocked(self):
        self.plan["personal_data_approved"] = False
        self.assertIn("personal_data_not_approved", review_pilot(self.plan)["issues"])
    def test_no_baseline_blocks(self):
        self.plan["baseline_metric"] = None
        self.assertEqual(review_pilot(self.plan)["state"], "PILOT_BLOCKED")
    def test_production_request_not_approved(self):
        self.plan["production_deployment_requested"] = True
        self.assertIn("production_requires_separate_approval", review_pilot(self.plan)["issues"])

if __name__ == "__main__":
    unittest.main()
