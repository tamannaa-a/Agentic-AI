# agents/explainer.py
def generate_explanation(extracted: dict, validation: dict, fraud: dict) -> dict:
    # Local templated explanation only (no external API)
    expl = []
    expl.append(f"Claim summary: detected {len(extracted.get('keywords', []))} keywords; amount: {extracted.get('claim_amount')}")
    if validation.get('covered'):
        expl.append("Policy coverage: The claim appears to fall under covered events.")
    else:
        expl.append("Policy coverage: The claim does not clearly match standard covered events — please review matched coverages.")

    amt = extracted.get('claim_amount') or 0.0
    if not validation.get('within_limit'):
        expl.append(f"Note: claimed amount ({amt}) exceeds policy limit of {validation['policy_stub']['limit']} — this may be reduced.")

    if fraud.get('score', 0) > 0.6:
        expl.append(f"Fraud risk: The system flagged a higher risk (score {fraud['score']:.2f}). Manual review recommended.")
    else:
        expl.append(f"Fraud risk: The system flagged low to medium risk (score {fraud['score']:.2f}).")

    expl.append(f"Missing fields: {', '.join(validation.get('missing_fields', [])) or 'None'}")

    # return a dict for compatibility with frontend
    return {'explanation': '\n'.join(expl), 'source': 'template'}
