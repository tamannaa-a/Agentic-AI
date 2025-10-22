import streamlit as st
import requests
from io import BytesIO

# -------------------------------
# App Page Config
# -------------------------------
st.set_page_config(
    page_title="Agentic AI - Document Classifier",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# App Header
# -------------------------------
st.markdown("""
    <h1 style='text-align:center;color:#2F80ED;'>🤖 Agentic AI - Document Classifier</h1>
    <p style='text-align:center;color:gray;'>Upload any insurance document (invoice, claim form, inspection report) and let AI auto-classify it!</p>
""", unsafe_allow_html=True)

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("📄 Upload a PDF document", type=["pdf"])

backend_url = "https://agentic-ai-1-5r73.onrender.com/predict"  # Your Render backend

if uploaded_file:
    st.info("🔍 Uploading and analyzing your document... please wait.")
    
    try:
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(backend_url, files={"file": uploaded_file})
        
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Document classified successfully!")

            # -------------------------------
            # 🔹 Display Results
            # -------------------------------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📘 Classification Result")
                st.metric("Document Type", result.get("document_type", "Unknown"))
                st.progress(min(int(float(result.get("confidence", "0").replace("%",""))),100))

            with col2:
                st.subheader("📋 Extracted Fields")
                fields = result.get("fields", {})
                if fields:
                    for k, v in fields.items():
                        st.markdown(f"**{k}:** {v}")
                else:
                    st.write("No additional fields extracted.")

            # -------------------------------
            # Show Uploaded File Preview
            # -------------------------------
            with st.expander("🧾 View PDF Info"):
                st.write(f"File Name: {uploaded_file.name}")
                st.write(f"File Size: {uploaded_file.size/1024:.2f} KB")

        else:
            st.error(f"Error from backend: {response.status_code}")

    except Exception as e:
        st.error(f"Failed to classify document: {e}")

else:
    st.info("⬆️ Please upload a PDF file to get started.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<hr>
<p style='text-align:center;color:gray;font-size:13px;'>
</p>
""", unsafe_allow_html=True)
