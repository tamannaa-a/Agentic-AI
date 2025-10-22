import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import tempfile
import numpy as np
import pdfplumber
import pytesseract
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import Dict

# config
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/data/uploads")
INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "/data/faiss.index")
META_PATH = os.environ.get("FAISS_META_PATH", "/data/faiss_meta.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

app = FastAPI(title="Document Classification API")

# Allow CORS from your frontend origin(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple model loader (Sentence-Transformers)
MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
print("Loading embedding model:", MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)

# categories (example)
CATEGORIES = {
    "Invoice": "invoice billing amount due total invoice number",
    "Claim Form": "insurance claim policy number claimant incident",
    "Inspection Report": "inspection report damage findings assessor"
}

# prepare category embeddings and FAISS index for categories (small)
category_names = list(CATEGORIES.keys())
category_texts = [CATEGORIES[c] for c in category_names]
category_embeddings = model.encode(category_texts, convert_to_numpy=True).astype("float32")
cat_index = faiss.IndexFlatL2(category_embeddings.shape[1])
cat_index.add(category_embeddings)

# Optionally: persistent FAISS index for documents (for searching DB of documents)
# We'll show how to save/load simple index for quick classification later.

def extract_text_from_pdf_path(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # OCR fallback for scanned page
                page_image = page.to_image(resolution=200).original
                text += pytesseract.image_to_string(page_image) + "\n"
    return text.strip()

class ClassifyResult(BaseModel):
    label: str
    confidence: float
    fields: Dict[str, str]
    text_preview: str

def extract_fields_simple(text: str):
    import re
    fields = {}
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}-\d{2}-\d{2})', text)
    amt_match = re.search(r'([\$₹]\s?\d+[.,]?\d*)', text)
    name_match = re.search(r'(?i)(?:Name|Customer|Insured)[:\s]*([A-Z][a-z]+\s?[A-Z]?[a-z]+)', text)
    fields["date"] = date_match.group(0) if date_match else ""
    fields["amount"] = amt_match.group(0) if amt_match else ""
    fields["name"] = name_match.group(1) if name_match else ""
    return fields

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Document Classification API healthy"}

@app.post("/classify", response_model=ClassifyResult)
async def classify_file(file: UploadFile = File(...)):
    # Save uploaded file
    suffix = os.path.splitext(file.filename)[1].lower()
    tmp_path = os.path.join(UPLOAD_DIR, f"{next(tempfile._get_candidate_names())}{suffix}")
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract text
    try:
        text = extract_text_from_pdf_path(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {e}")

    if not text or len(text.strip()) < 10:
        # unreadable — return helpful error
        raise HTTPException(status_code=400, detail="No readable text found in document")

    # chunk embedding approach (to avoid averaging long doc to nonsense)
    CHUNK_SIZE = 512
    chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE) if text[i:i+CHUNK_SIZE].strip()]
    chunk_emb = model.encode(chunks, convert_to_numpy=True).astype("float32")  # (num_chunks, dim)

    # compute similarity to categories (mean similarity over chunks)
    sims = []
    for c_emb in category_embeddings:
        # dot product / cosine (we can compute cosine quickly)
        # compute cosine similarity
        # normalize
        chunk_norms = np.linalg.norm(chunk_emb, axis=1, keepdims=True)
        c_emb_norm = np.linalg.norm(c_emb)
        # avoid division by zero
        denom = chunk_norms * (c_emb_norm + 1e-12)
        cosine = (chunk_emb @ c_emb.reshape(-1,1)).squeeze() / (denom.squeeze() + 1e-12)
        sims.append(float(np.mean(cosine)))
    best_idx = int(np.argmax(sims))
    label = category_names[best_idx]
    confidence = float(sims[best_idx])  # between -1 and 1

    # extract some fields
    fields = extract_fields_simple(text)

    # prepare preview
    preview = text[:1500]

    return ClassifyResult(label=label, confidence=confidence, fields=fields, text_preview=preview)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
