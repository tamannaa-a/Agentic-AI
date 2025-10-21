from fastapi import FastAPI, UploadFile
import pdfplumber
import joblib

app = FastAPI(title="Document Classification Agent")

# Load model
model = joblib.load("document_classifier.pkl")

@app.get("/")
def home():
    return {"message": "Welcome to the Document Classification API"}

@app.post("/predict")
async def predict(file: UploadFile):
    # Extract text from uploaded PDF
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""

    # Predict document type
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    confidence = max(probabilities) * 100

    return {"document_type": prediction, "confidence": f"{confidence:.2f}%"}
