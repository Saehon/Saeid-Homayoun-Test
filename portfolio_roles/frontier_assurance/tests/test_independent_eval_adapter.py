import unittest
from portfolio_roles.frontier_assurance.independent_eval_adapter import assess

class TestIndependentEval(unittest.TestCase):
    def setUp(self):
        self.gold = [{"case_id":"SYN-01","gold_label":1,"independent_labeler_id":"reviewer",
                      "label_protocol":"SYN-v1","evidence_id":"E1"},
                     {"case_id":"SYN-02","gold_label":0,"independent_labeler_id":"reviewer",
                      "label_protocol":"SYN-v1","evidence_id":"E2"}]
    def test_multiple_candidate_comparison(self):
        report=assess(self.gold,{"A":[{"case_id":"SYN-01","predicted_label":1},
                                      {"case_id":"SYN-02","predicted_label":0}],
                                 "B":[{"case_id":"SYN-01","predicted_label":0},
                                      {"case_id":"SYN-02","predicted_label":1}]})
        self.assertEqual(report["comparison"]["A"]["answered_accuracy"],1.0)
        self.assertEqual(report["comparison"]["B"]["answered_accuracy"],0.0)
    def test_holdout_contamination_fails_closed(self):
        with self.assertRaises(ValueError):
            assess(self.gold,{},dev_ids=["SYN-01"])
    def test_missing_independence_metadata_blocked(self):
        del self.gold[0]["independent_labeler_id"]
        with self.assertRaises(ValueError):
            assess(self.gold,{})
    def test_float_gold_label_rejected(self):
        self.gold[0]["gold_label"] = 1.0
        with self.assertRaises(ValueError):
            assess(self.gold,{})

    def test_abstentions_counted(self):
        report=assess(self.gold,{"A":[{"case_id":"SYN-01","predicted_label":1}]})
        self.assertEqual(report["comparison"]["A"]["abstentions"],1)

if __name__ == "__main__":
    unittest.main()
