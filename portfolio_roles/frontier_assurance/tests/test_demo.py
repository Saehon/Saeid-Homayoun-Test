import unittest
from portfolio_roles.frontier_assurance.demo import review_evaluation

class TestFrontierAssurance(unittest.TestCase):
    def setUp(self):
        self.record = {"evaluation_id": "E1", "model_id": "synthetic", "protocol_version": "v1",
                       "assessor": "independent", "model_team": "builders",
                       "public_method_url": "https://example.org", "evidence_id": "SYN-01",
                       "holdout_declared": True, "planned_tests": 4, "completed_tests": 4,
                       "unresolved_critical_findings": 0}

    def test_complete_record_ready_for_review(self):
        self.assertEqual(review_evaluation(self.record)["evidence_status"], "READY_FOR_INDEPENDENT_REVIEW")

    def test_conflict_of_interest_blocks(self):
        self.record["assessor"] = "builders"
        self.assertIn("assessor_conflict", review_evaluation(self.record)["gaps"])

    def test_partial_coverage_blocks(self):
        self.record["completed_tests"] = 3
        self.assertEqual(review_evaluation(self.record)["evidence_status"], "INSUFFICIENT_EVIDENCE")

    def test_missing_holdout_blocks(self):
        self.record["holdout_declared"] = False
        self.assertIn("holdout_not_documented", review_evaluation(self.record)["gaps"])

if __name__ == "__main__":
    unittest.main()
