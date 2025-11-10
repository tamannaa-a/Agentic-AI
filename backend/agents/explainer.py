# agents/explainer.py
import os

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

def build_prompt(extracted, validation, fraud):
    return (
        "You are an insurance claims assistant. Provide a concise explanation for the claim processing result.\n\n"
        f"Extracted: {extracted}\n"
        f"Validation: {validation}\n"
        f"Fraud: {fraud}\n\n"
        "Explain in plain language what the likely decision is, what adjustments may occur, and why manual review may be needed. Limit to 200 words."
    )

def generate_explanation(extracted: dict, validation: dict, fraud: dict) -> dict:
    if OPENAI_KEY:
        try:
            import openai
            openai.api_key = OPENAI_KEY
            prompt = build_prompt(extracted, validation, fraud)
            resp = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=400,
                temperature=0.2
            )
            text = resp['choices'][0]['message']['content'].strip()
            return {'explanation': text, 'source': 'openai'}
        except Exception as e:
            print('OpenAI call failed:', e)

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

    return {'explanation': '\n'.join(expl), 'source': 'template'}
