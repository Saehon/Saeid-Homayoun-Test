"""Offline comparison of externally labelled binary evaluation outputs.

Not a safety evaluation unless independent, admissible gold records and real
system predictions are supplied. Refuses overlapping development IDs.
"""
from __future__ import annotations
import json
from pathlib import Path

def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def unique(rows):
    result = {}
    for row in rows:
        key = str(row.get("case_id") or "")
        if not key or key in result:
            raise ValueError("missing or duplicate case_id")
        result[key] = row
    return result

def assess(gold_rows, prediction_sets, dev_ids=()):
    gold = unique(gold_rows)
    if not gold:
        raise ValueError("empty independent evaluation")
    overlap = set(gold).intersection(set(dev_ids))
    if overlap:
        raise ValueError(f"train/holdout contamination: {len(overlap)} IDs")
    for row in gold.values():
        if row.get("gold_label") not in (0, 1) or type(row.get("gold_label")) is bool:
            raise ValueError("gold_label must be binary integer")
        for field in ("independent_labeler_id", "label_protocol", "evidence_id"):
            if not row.get(field):
                raise ValueError("missing independent gold provenance: " + field)
    comparison = {}
    for name, predictions in prediction_sets.items():
        pred = unique(predictions)
        if set(pred) - set(gold):
            raise ValueError("unrecognized prediction IDs")
        tp = tn = fp = fn = abstain = 0
        for key, ref in gold.items():
            record = pred.get(key, {})
            label = record.get("predicted_label")
            if label is None:
                abstain += 1
                continue
            if type(label) is not int or label not in (0, 1):
                raise ValueError("prediction must be 0/1 or null")
            actual = ref["gold_label"]
            if label == 1 and actual == 1: tp += 1
            if label == 0 and actual == 0: tn += 1
            if label == 1 and actual == 0: fp += 1
            if label == 0 and actual == 1: fn += 1
        reviewed = tp + tn + fp + fn
        precision = tp/(tp+fp) if tp+fp else 0.
        recall = tp/(tp+fn) if tp+fn else 0.
        comparison[name] = {"n":len(gold), "answered":reviewed,
            "abstentions":abstain, "coverage":round(reviewed/len(gold),4),
            "answered_accuracy":round((tp+tn)/reviewed,4) if reviewed else None,
            "precision_positive":round(precision,4),
            "recall_positive":round(recall,4),
            "f1_positive":round(2*precision*recall/(precision+recall),4) if precision+recall else 0.,
            "tp":tp, "tn":tn, "fp":fp, "fn":fn}
    return {"comparison":comparison, "independence_is_claimed_not_verified":True,
            "human_review_required":True,
            "limitations":["Gold provenance is schema-validated, not independently authenticated.",
                           "Aggregate scores cannot justify safety or deployment approval."]}

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--gold",required=True)
    p.add_argument("--pred",action="append",required=True,help="NAME=path")
    p.add_argument("--dev-ids",default=None,help="optional JSON file of development-case IDs")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    results={}
    for spec in a.pred:
        name, sep, path=spec.partition("=")
        if not sep or not name or not path or name in results:
            p.error("unique NAME=path required")
        results[name]=read_jsonl(path)
    overlap=json.loads(Path(a.dev_ids).read_text()) if a.dev_ids else []
    result=assess(read_jsonl(a.gold),results,overlap)
    output=Path(a.out);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(output)
