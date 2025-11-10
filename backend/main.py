# main.py
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from typing import Optional
from agents.extractor import extract_entities_from_file
from agents.validator import validate_against_policy
from agents.fraud_analyzer import predict_fraud_score
from agents.explainer import generate_explanation

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title='Intelligent Claims Orchestrator')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/analyze')
async def analyze_claim(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    policy_id: Optional[str] = Form(None)
):
    filepath = None
    filename = None
    if file is not None:
        filename = file.filename
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        filepath = path

    extracted = extract_entities_from_file(filepath or '', text_override=text)

    policy_stub = None
    validation = validate_against_policy(extracted, policy_stub)

    features = {
        'claim_amount': extracted.get('claim_amount', 0.0),
        'num_prior_claims': 0,
        'days_since_policy_start': 365,
        'suspicious_keyword_count': len(extracted.get('keywords', []))
    }
    fraud = predict_fraud_score(features)

    explanation = generate_explanation(extracted, validation, fraud)

    nodes = [
        {'id': 'uploader', 'label': 'Uploader', 'meta': {'filename': filename}},
        {'id': 'extractor', 'label': 'Extractor', 'meta': extracted},
        {'id': 'validator', 'label': 'Validator', 'meta': validation},
        {'id': 'fraud', 'label': 'Fraud Analyzer', 'meta': fraud},
        {'id': 'explainer', 'label': 'Explainer', 'meta': explanation}
    ]
    edges = [
        {'from': 'uploader', 'to': 'extractor'},
        {'from': 'extractor', 'to': 'validator'},
        {'from': 'validator', 'to': 'fraud'},
        {'from': 'fraud', 'to': 'explainer'}
    ]

    response = {
        'extracted': extracted,
        'validation': validation,
        'fraud': fraud,
        'explanation': explanation,
        'graph': {'nodes': nodes, 'edges': edges}
    }

    return JSONResponse(response)

@app.get('/health')
async def health():
    return {'status': 'ok'}
