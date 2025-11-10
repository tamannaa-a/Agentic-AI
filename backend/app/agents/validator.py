from typing import Dict

def validate_against_policy(extracted: Dict, policy_stub: Dict = None) -> Dict:
    if policy_stub is None:
        policy_stub = {
            "coverages": ["collision", "theft", "fire", "flood"],
            "limit": 100000.0,
            "deductible": 500.0,
        }
    verdict = {}
    kws = extracted.get("keywords", [])
    matched = [k for k in kws if k in policy_stub["coverages"]]
    verdict["covered"] = len(matched) > 0
    verdict["matched_coverages"] = matched
    amount = extracted.get("claim_amount") or 0.0
    verdict["within_limit"] = amount <= policy_stub["limit"]
    verdict["deductible"] = policy_stub["deductible"]
    missing = []
    if "claim_id" not in extracted:
        missing.append("claim_id")
    if "date" not in extracted:
        missing.append("date")
    verdict["missing_fields"] = missing
    verdict["policy_stub"] = policy_stub
    return verdict
