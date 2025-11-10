# Intelligent Claims Orchestrator (Local)

A full-stack local project: multi-agent claims orchestrator (Extractor → Validator → Fraud Analyzer → Explainer) + React frontend with a D3 decision graph.

## Quick start (Linux / macOS)

1. Backend
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python train_fraud_model.py
   uvicorn main:app --reload --port 8000

2. Frontend (new terminal)
   cd frontend
   npm install
   npm run dev

Open http://localhost:5173 and test.

## Push to GitHub
git init
git add .
git commit -m "Initial commit"
# create repo on GitHub, then:
git remote add origin https://github.com/<your-username>/intelligent-claims-orchestrator.git
git branch -M main
git push -u origin main

Download ZIP from GitHub: Repo → Code → Download ZIP
