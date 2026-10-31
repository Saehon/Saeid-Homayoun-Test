"""University LLM pilot unit-economics scenario. All prices must be user-supplied."""
from decimal import Decimal, InvalidOperation

def d(value):
    x = Decimal(str(value))
    if not x.is_finite() or x < 0:
        raise ValueError("finite nonnegative values required")
    return x

def estimate_scenario(values):
    fields=("requests_per_month", "prompt_tokens_per_request", "completion_tokens_per_request",
            "input_price_per_million", "output_price_per_million",
            "retrieval_cost_per_request", "human_review_minutes_per_request",
            "reviewer_hourly_cost", "fixed_monthly_infrastructure_cost")
    if any(k not in values for k in fields):
        raise ValueError("incomplete scenario")
    params={k:d(values[k]) for k in fields}
    n=params["requests_per_month"]
    token_cost=n*(params["prompt_tokens_per_request"]*params["input_price_per_million"]+
                  params["completion_tokens_per_request"]*params["output_price_per_million"])/Decimal(1_000_000)
    retrieval=n*params["retrieval_cost_per_request"]
    human=n*params["human_review_minutes_per_request"]*params["reviewer_hourly_cost"]/Decimal(60)
    fixed=params["fixed_monthly_infrastructure_cost"]
    total=token_cost+retrieval+human+fixed
    return {"monthly_total":str(total), "tokens":str(token_cost),
            "retrieval":str(retrieval), "human_review":str(human), "fixed":str(fixed),
            "cost_per_request":str(total/n) if n else None,
            "currency":values.get("currency", "unspecified"),
            "assumptions_not_verified":True, "causal_roi_estimated":False}

if __name__=="__main__":
    example={"requests_per_month":1000,"prompt_tokens_per_request":1000,
             "completion_tokens_per_request":200,"input_price_per_million":2,
             "output_price_per_million":10,"retrieval_cost_per_request":"0.01",
             "human_review_minutes_per_request":"0.25","reviewer_hourly_cost":40,
             "fixed_monthly_infrastructure_cost":100,"currency":"USD"}
    import json
    print(json.dumps(estimate_scenario(example),indent=2))
