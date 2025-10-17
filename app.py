import streamlit as st
import pdfplumber
from PIL import Image
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pytesseract
import io
import base64

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Document Classifier AI", page_icon="📄", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .reportview-container {
            background: linear-gradient(180deg, #f9f9f9, #e3f2fd);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            font-size: 1em;
        }
        .stProgress > div > div {
            background-color: #2196F3;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# MODEL LOAD
# -----------------------------
@st.cache_resource
def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

model = load_model()

# -----------------------------
# DOCUMENT TYPES
# -----------------------------
doc_types = [
    "Claim Form",
    "Inspection Report",
    "Invoice",
    "Policy Document",
    "Other"
]
doc_embeddings = model.encode(doc_types)

index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(np.array(doc_embeddings))

# -----------------------------
# UPLOAD SECTION
# -----------------------------
st.title("📄 Smart Document Classification AI")
st.markdown("### Upload your document — the AI will identify what type it is!")

uploaded_file = st.file_uploader("Upload a PDF or Image file", type=["pdf", "png", "jpg", "jpeg"])

# -----------------------------
# FUNCTION: Extract Text
# -----------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = " ".join([page.extract_text() or "" for page in pdf.pages])
    else:
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
    return text.strip()

# -----------------------------
# PROCESS BUTTON
# -----------------------------
if uploaded_file is not None:
    st.info("File uploaded successfully!")

    if st.button("🔍 Classify Document"):
        with st.spinner("Analyzing your document... 🧠"):
            text = extract_text(uploaded_file)
            if len(text) < 20:
                st.error("Document text is too short or unreadable. Try a clearer file.")
            else:
                query_vec = model.encode([text])
                distances, indices = index.search(query_vec, 1)
                predicted_type = doc_types[indices[0][0]]
                confidence = round((1 - distances[0][0]) * 100, 2)

                st.success(f" Document Type: **{predicted_type}**")
                st.metric("Confidence", f"{confidence} %")

                if confidence > 80:
                    st.balloons()
                elif confidence > 60:
                    st.progress(70)
                else:
                    st.warning("⚠️ Confidence is low — document may be unclear or mixed.")

                with st.expander("📄 View Extracted Text"):
                    st.text_area("Extracted Content", text[:2000])

else:
    st.info("👆 Upload a file above to get started.")

# -----------------------------
# SIDEBAR INFO
# -----------------------------
st.sidebar.header("About This App")
st.sidebar.write("""
This **AI-powered Document Classifier** can detect whether a file is:
- 🧾 Claim Form  
- 🔍 Inspection Report  
- 💰 Invoice  
- 📘 Policy Document  
- 🗂️ Others  

Built using:
- `Sentence Transformers`
- `FAISS`
- `Streamlit`
- `pdfplumber` + `OCR`
""")

st.sidebar.markdown("---")
