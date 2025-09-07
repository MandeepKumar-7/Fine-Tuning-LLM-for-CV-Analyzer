
import streamlit as st
from scripts.ocr_extraction import extract_text_from_pdf_bytes
from scripts.parse_fields import extract_fields
from scripts.qna_generation import generate_qna

st.set_page_config(page_title="CV Analyzer LLM", page_icon="📄", layout="centered")
st.title("📄 CV Analyzer LLM")

uploaded = st.file_uploader("Upload a CV (PDF)", type=["pdf"])
if uploaded:
    pdf_bytes = uploaded.read()
    with st.spinner("Running OCR..."):
        text = extract_text_from_pdf_bytes(pdf_bytes)

    st.subheader("Extracted Text (first 1000 chars)")
    st.code(text[:1000] + ("..." if len(text) > 1000 else ""), language="markdown")

    fields = extract_fields(text)
    st.subheader("Parsed Fields")
    st.json(fields)

    st.subheader("Automated Q&A (Prompt-style, heuristic answers)")
    qna_items = list(generate_qna(text))
    for item in qna_items:
        st.markdown(f"**Q:** {item['question']}\n\n**A:** {item['answer']}")
else:
    st.info("Upload a PDF resume to begin.")
