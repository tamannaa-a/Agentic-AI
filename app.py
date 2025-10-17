import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
from io import BytesIO
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

# -------------------------------
# 🌟 Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Agentic AI - Smart Document Classifier",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# 🎨 Custom Styling
# -------------------------------
st.markdown("""
    <style>
        .stApp { background-color: #F9FAFB; }
        h1 { text-align: center; color: #2F80ED; }
        .desc { text-align: center; color: #6C757D; font-size: 16px; margin-bottom: 30px; }
        .result-box {
            background-color: #E3F2FD;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
        }
        .footer {
            text-align: center; color: gray; font-size: 13px; margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧠 Title Section
# -------------------------------
st.markdown("<h1>🤖 Agentic AI - Smart Document Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='desc'>Upload any insurance document — Invoice, Claim Form, or Inspection Report — and let AI classify it automatically.</p>", unsafe_allow_html=True)

# -------------------------------
# 🔹 Load Embedding Model
# -------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# -------------------------------
# 🔹 Predefined Categories
# -------------------------------
categories = {
    "Invoice": [
        "invoice", "bill", "amount due", "subtotal", "tax", "payment terms", "billed to"
    ],
    "Claim Form": [
        "insurance claim", "policy number", "incident details", "claim type",
        "insured name", "loss description", "signature of claimant"
    ],
    "Inspection Report": [
        "inspection report", "vehicle assessment", "inspection date",
        "damage description", "inspector name", "findings", "recommendations"
    ],
}

# -------------------------------
# 📄 Extract Text (with OCR fallback)
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if not page_text:  # If no text, try OCR
                img = page.to_image(resolution=200).original
                page_text = pytesseract.image_to_string(img)
            text += page_text or ""
    return text.strip()

# -------------------------------
# 🤖 Improved Classification
# -------------------------------
def classify_document(text):
    if not text or len(text.strip()) == 0:
        return "Unreadable Document", 0.0, {}

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    if not chunks:
        return "Unreadable Document", 0.0, {}

    chunk_embeddings = model.encode(chunks, convert_to_numpy=True)
    category_scores = {}

    for cat, keywords in categories.items():
        cat_embedding = model.encode([" ".join(keywords)], convert_to_numpy=True)
        similarities = np.dot(chunk_embeddings, cat_embedding.T) / (
            np.linalg.norm(chunk_embeddings, axis=1, keepdims=True) * np.linalg.norm(cat_embedding)
        )
        category_scores[cat] = float(np.mean(similarities))

    best_label = max(category_scores, key=category_scores.get)
    confidence = round(category_scores[best_label], 3)
    return best_label, confidence, category_scores

# -------------------------------
# 🔍 Extract Important Fields
# -------------------------------
def extract_fields(text):
    fields = {}
    date_match = re.search(r"\b\d{2,4}[/-]\d{2}[/-]\d{2,4}\b", text)
    amount_match = re.search(r"[\$₹]\s?\d+[,.]?\d*", text)
    name_match = re.search(r"(?i)(?:Name|Customer|Client|Insured)[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)

    fields["Date"] = date_match.group(0) if date_match else "Not found"
    fields["Amount"] = amount_match.group(0) if amount_match else "Not found"
    fields["Name"] = name_match.group(1) if name_match else "Not found"
    return fields

# -------------------------------
# 📤 File Upload
# -------------------------------
uploaded_file = st.file_uploader("📁 Upload a PDF document", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Analyzing your document... Please wait"):
        text = extract_text_from_pdf(uploaded_file)
        label, confidence, scores = classify_document(text)
        fields = extract_fields(text)

    st.success("✅ Document analyzed successfully!")

    # -------------------------------
    # 🧾 Show Results
    # -------------------------------
    st.markdown(f"<div class='result-box'><b>Predicted Document Type:</b> {label}<br><b>Confidence:</b> {confidence}</div>", unsafe_allow_html=True)

    # -------------------------------
    # 📊 Confidence Chart
    # -------------------------------
    if scores:
        st.subheader("📈 Category Confidence Overview")
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.barh(list(scores.keys()), list(scores.values()), color=["#4CAF50", "#2196F3", "#FF9800"])
        ax.set_xlabel("Similarity Score")
        ax.set_title("Category Confidence Levels")
        st.pyplot(fig)

    # -------------------------------
    # 🗂️ Extracted Info
    # -------------------------------
    st.subheader("📋 Extracted Key Fields")
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 Date", fields["Date"])
    col2.metric("💰 Amount", fields["Amount"])
    col3.metric("🧍 Name", fields["Name"])

    # -------------------------------
    # 🧠 Text Preview
    # -------------------------------
    with st.expander("📜 View Extracted Text"):
        st.text_area("Extracted Text", text[:2000] + "...", height=250)

else:
    st.info("⬆️ Please upload a PDF to begin analysis.")

# -------------------------------
# 💬 Footer
# -------------------------------
st.markdown("""
<hr>
<p class='footer'>
Built with ❤️ using Streamlit & SentenceTransformers | Agentic AI © 2025
</p>
""", unsafe_allow_html=True)
