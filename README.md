# Intelligent Claims Orchestrator — Industry-ready local demo

## Overview
A production-style, offline-capable claims orchestration demo:
- Backend: FastAPI agents (Extractor, Validator, Fraud Analyzer, Explainer)
- Frontend: React + Vite + Tailwind + Recharts + D3 for a professional dashboard
- Fully offline — no API keys required

## Run locally (Windows cmd)
1. Backend
   cd backend
   python -m venv venv
   venv\Scripts\activate.bat
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python app/train_fraud_model.py
   python -m uvicorn app.main:app --reload --port 8000

2. Frontend (new terminal)
   cd frontend
   npm install
   npm run dev
   Open http://localhost:5173

## Docker
docker-compose up --build

## Notes
- Model is synthetic (train_fraud_model.py). Replace with real training for production.
- For production: add auth, TLS, logging aggregation, persistent DB, CI/CD.
