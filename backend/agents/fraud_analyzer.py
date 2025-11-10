# agents/fraud_analyzer.py
import joblib
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'fraud_model.joblib')
clf = None
if os.path.exists(MODEL_PATH):
    try:
        clf = joblib.load(MODEL_PATH)
    except Exception:
        clf = None

def predict_fraud_score(features: dict) -> dict:
    f = {
        'claim_amount': float(features.get('claim_amount', 0.0) or 0.0),
        'num_prior_claims': int(features.get('num_prior_claims', 0) or 0),
        'days_since_policy_start': float(features.get('days_since_policy_start', 365.0) or 365.0),
        'suspicious_keyword_count': int(features.get('suspicious_keyword_count', 0) or 0)
    }
    X = np.array([[f['claim_amount'], f['num_prior_claims'], f['days_since_policy_start'], f['suspicious_keyword_count']]])
    if clf is None:
        score = min(1.0, (0.00005 * f['claim_amount']) + (0.2 * f['suspicious_keyword_count']))
        pred = 1 if score > 0.5 else 0
        return {'score': float(score), 'pred': int(pred), 'model': 'heuristic'}
    try:
        prob = float(clf.predict_proba(X)[0][1])
        pred = int(prob > 0.5)
        return {'score': prob, 'pred': pred, 'model': 'random_forest'}
    except Exception:
        score = min(1.0, (0.00005 * f['claim_amount']) + (0.2 * f['suspicious_keyword_count']))
        pred = 1 if score > 0.5 else 0
        return {'score': float(score), 'pred': int(pred), 'model': 'heuristic-fallback'}
