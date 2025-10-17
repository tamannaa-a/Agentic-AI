import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
from io import BytesIO
from PIL import Image

# -------------------------------
# App Title and Description
# -------------------------------
st.set_page_config(page_title="Agentic AI - Document Classifier", page_icon="🤖", layout="wide")

st.markdown("""
    <h1 style='text-align:center;color:#2F80ED;'>🤖 Agentic AI - Smart Document Classifier</h1>
    <p style='text-align:center;color:gray;'>Upload any insurance document (invoice, claim form, inspection report) and let AI auto-classify it!</p>
""", unsafe_allow_html=True)

# -------------------------------
# Load Embedding Model
# -------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# -------------------------------
# Predefined Categories
# -------------------------------
categories = {
    "Invoice": ["invoice", "amount due", "total payable", "bill no", "payment terms"],
    "Claim Form": ["claim number", "policy holder", "insurance claim", "incident", "policy no"],
    "Inspection Report": ["vehicle inspection", "report", "assessment", "damages", "inspector"],
}

# -------------------------------
# Utility Functions
# -------------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def classify_document(text):
    # Convert category samples to embeddings
    category_names = list(categories.keys())
    sample_sentences = [" ".join(categories[c]) for c in category_names]
    sample_embeddings = model.encode(sample_sentences, convert_to_numpy=True)
    query_embedding = model.encode([text], convert_to_numpy=True)

    # Use FAISS for similarity
    index = faiss.IndexFlatL2(sample_embeddings.shape[1])
    index.add(sample_embeddings)
    distances, indices = index.search(query_embedding, 1)
    return category_names[indices[0][0]], distances[0][0]

def extract_fields(text):
    fields = {}
    date_match = re.search(r"\b\d{2,4}[/-]\d{2}[/-]\d{2,4}\b", text)
    amount_match = re.search(r"[\$₹]\s?\d+[,.]?\d*", text)
    name_match = re.search(r"(?i)(?:Name|Customer|Client)[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)

    fields["Date"] = date_match.group(0) if date_match else "Not found"
    fields["Amount"] = amount_match.group(0) if amount_match else "Not found"
    fields["Name"] = name_match.group(1) if name_match else "Not found"
    return fields

# -------------------------------
# Upload Section
# -------------------------------
uploaded_file = st.file_uploader("📄 Upload a PDF document", type=["pdf"])

if uploaded_file:
    with st.spinner("🔍 Analyzing document..."):
        text = extract_text_from_pdf(uploaded_file)
        label, score = classify_document(text)
        fields = extract_fields(text)

    st.success("Document processed successfully!")

    # -------------------------------
    # Display Results
    # -------------------------------
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📘 Classification Result")
        st.markdown(f"**Predicted Type:** `{label}`")
        st.markdown(f"**Confidence (lower = better):** `{round(score, 2)}`")

    with col2:
        st.subheader("📋 Extracted Key Fields")
        for k, v in fields.items():
            st.markdown(f"**{k}:** {v}")

    # -------------------------------
    # Text Summary Preview
    # -------------------------------
    with st.expander("🧠 View Extracted Text"):
        st.text_area("Document Text", text[:2000] + "...", height=200)

else:
    st.info("⬆️ Please upload a PDF file to get started.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<hr>
<p style='text-align:center;color:gray;font-size:13px;'>
Built with ❤️ using Streamlit & SentenceTransformers | Agentic AI 2025
</p>
""", unsafe_allow_html=True)
