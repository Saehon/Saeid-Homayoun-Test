import unittest
from portfolio_roles.openai_education_architect.cost_model import estimate_scenario

class TestEducationCost(unittest.TestCase):
    def setUp(self):
        self.a = {"requests_per_month":1000,"prompt_tokens_per_request":1000,
                  "completion_tokens_per_request":1000,"input_price_per_million":1,
                  "output_price_per_million":2,"retrieval_cost_per_request":0,
                  "human_review_minutes_per_request":0,"reviewer_hourly_cost":0,
                  "fixed_monthly_infrastructure_cost":0}
    def test_token_arithmetic(self):
        r=estimate_scenario(self.a)
        self.assertEqual(r["monthly_total"],"3")
        self.assertFalse(r["causal_roi_estimated"])
    def test_zero_queries_explicit_denominator(self):
        self.a["requests_per_month"]=0
        self.assertIsNone(estimate_scenario(self.a)["cost_per_request"])
    def test_negative_cost_rejected(self):
        self.a["input_price_per_million"]=-1
        with self.assertRaises(ValueError):
            estimate_scenario(self.a)
    def test_missing_price_rejected(self):
        del self.a["output_price_per_million"]
        with self.assertRaises(ValueError):
            estimate_scenario(self.a)
if __name__=="__main__":
    unittest.main()
