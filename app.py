# ==========================================================
# Document Classification Agentic AI - Streamlit App
# ==========================================================
# Author: Tamanna (Customized by ChatGPT)
# Description:
# Upload PDFs → Extract text (OCR/Text) → Classify (Invoice/Claim/Report)
# ==========================================================

import streamlit as st
import pdfplumber
from PIL import Image
import pytesseract
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ----------------------------------------------------------
# 🛠 Step 1: Setup Page
# ----------------------------------------------------------
st.set_page_config(
    page_title="📄 Document Classifier AI",
    page_icon="🤖",
    layout="centered"
)

st.title("📑 Document Classification Agentic AI")
st.markdown("""
Welcome! This tool automatically classifies uploaded insurance documents such as:
- 🧾 **Invoices**
- 🏥 **Claim Forms**
- 🕵️ **Inspection Reports**

Simply upload a PDF below 👇
""")

# ----------------------------------------------------------
# Step 2: Configure Tesseract OCR (for image-based PDFs)
# ----------------------------------------------------------
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Default Windows path
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    ocr_enabled = True
    st.success("✅ Tesseract OCR found and configured!")
else:
    ocr_enabled = False
    st.warning("⚠️ Tesseract not found! OCR features will be disabled.")
    st.info("Install it from [Tesseract OCR (UB Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)")

# ----------------------------------------------------------
# 📚 Step 3: Load Sentence Embedding Model
# ----------------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()
st.sidebar.success("✅ Model loaded successfully!")

# ----------------------------------------------------------
# Step 4: Define Reference Documents
# ----------------------------------------------------------
reference_texts = {
    "Invoice": "This invoice includes billing details, payment terms, and itemized costs for services rendered.",
    "Claim Form": "The claim form includes policy number, claimant information, and incident description for insurance processing.",
    "Inspection Report": "This report includes observations, findings, and photos from an inspection visit."
}

reference_embeddings = np.array([model.encode(text) for text in reference_texts.values()]).astype("float32")
index = faiss.IndexFlatL2(reference_embeddings.shape[1])
index.add(reference_embeddings)

# ----------------------------------------------------------
# Step 5: PDF Upload
# ----------------------------------------------------------
uploaded_file = st.file_uploader("📤 Upload a PDF document", type=["pdf"])

# ----------------------------------------------------------
# Step 6: Text Extraction Function
# ----------------------------------------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
            elif ocr_enabled:
                # OCR fallback for scanned pages
                image = page.to_image(resolution=300).original
                text += pytesseract.image_to_string(image)
    return text

# ----------------------------------------------------------
# Step 7: Classification Logic
# ----------------------------------------------------------
if uploaded_file is not None:
    with st.spinner("⏳ Extracting and classifying document..."):
        pdf_text = extract_text_from_pdf(uploaded_file)

        if len(pdf_text.strip()) == 0:
            st.error("❌ Could not extract any text from the document.")
        else:
            # Get embedding and classify
            query_embedding = model.encode([pdf_text]).astype("float32")
            distances, indices = index.search(query_embedding, k=1)
            predicted_label = list(reference_texts.keys())[indices[0][0]]

            # Display result
            st.success(f"✅ Document classified as: **{predicted_label}**")
            st.markdown("---")
            with st.expander("📜 Extracted Text (click to expand)"):
                st.text(pdf_text[:1500])  # limit to first 1500 chars
else:
    st.info("👆 Upload a PDF to begin classification.")

# ----------------------------------------------------------
# Footer
# ----------------------------------------------------------
st.markdown("""
---
💡 **Tips:**
- If your PDF is scanned, make sure Tesseract is installed for OCR.
- Works best with clear text or structured PDF files.
- Want to deploy on GitHub + Streamlit Cloud?  
  → Push this `app.py` and requirements.txt to your repo!

""")
