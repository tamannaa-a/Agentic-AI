from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.agents.extractor import extract_entities_from_file
from app.agents.validator import validate_against_policy
from app.agents.fraud_analyzer import predict_fraud_score
from app.agents.explainer import generate_explanation
from app.core.config import settings
from app.core.logger import logger
import os, shutil

router = APIRouter(prefix="/claims", tags=["Claims"])

@router.post("/analyze")
async def analyze_claim(file: UploadFile = File(None), text: str = Form(None)):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filepath = None
    filename = None
    if file:
        filename = file.filename
        filepath = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved uploaded file: {filepath}")

    extracted = extract_entities_from_file(filepath or "", text_override=text)
    logger.info(f"Extracted keys: {list(extracted.keys())}")

    validation = validate_against_policy(extracted)
    features = {
        "claim_amount": extracted.get("claim_amount", 0.0),
        "num_prior_claims": 0,
        "days_since_policy_start": 365,
        "suspicious_keyword_count": len(extracted.get("keywords", [])),
    }
    fraud = predict_fraud_score(features)
    explanation = generate_explanation(extracted, validation, fraud)

    nodes = [
        {"id": "uploader", "label": "Uploader", "meta": {"filename": filename}},
        {"id": "extractor", "label": "Extractor", "meta": extracted},
        {"id": "validator", "label": "Validator", "meta": validation},
        {"id": "fraud", "label": "Fraud Analyzer", "meta": fraud},
        {"id": "explainer", "label": "Explainer", "meta": explanation}
    ]
    edges = [
        {"from": "uploader", "to": "extractor"},
        {"from": "extractor", "to": "validator"},
        {"from": "validator", "to": "fraud"},
        {"from": "fraud", "to": "explainer"}
    ]

    response = {
        "extracted": extracted,
        "validation": validation,
        "fraud": fraud,
        "explanation": explanation,
        "graph": {"nodes": nodes, "edges": edges}
    }

    return JSONResponse(response)
