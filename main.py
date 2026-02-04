import streamlit as st
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher

st.set_page_config(page_title="MAKO | Agentic Hub", layout="wide")

if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# SIDEBAR
with st.sidebar:
    st.title("🦅 MAKO Console")
    mode = st.radio("Task:", ["📚 Notes", "✍️ Mock Test", "⚖️ Audit"])
    st.divider()
    st.info("Ingesting: PDF, DOCX, Images")

# MAIN UI
st.title("Multi-Modal Knowledge Orchestrator")

col1, col2 = st.columns(2)
with col1:
    source_file = st.file_uploader("Upload Source (PDF/Docx/Image)", type=["pdf", "docx", "jpg", "png", "jpeg"])
with col2:
    if mode == "⚖️ Audit":
        evidence_file = st.file_uploader("Upload Student Work (PDF/Image)", type=["pdf", "jpg", "png", "jpeg"])
    else:
        st.write("Source-only mode active.")

if st.button(f"🚀 Execute {mode}"):
    if source_file:
        with st.spinner("Council Deliberating..."):
            context = DocumentProcessor.extract_text(source_file)
            agent = Researcher(st.session_state.handler)
            
            if mode == "📚 Notes":
                # Pass file for Vision if it's an image, else pass extracted text
                res = agent.generate_notes(context, source_file if "[IMAGE_UPLOADED]" in context else None)
            elif mode == "⚖️ Audit":
                evidence_text = DocumentProcessor.extract_text(evidence_file)
                res = agent.analyze(context, evidence_text, evidence_file if "[IMAGE_UPLOADED]" in evidence_text else None)
            
            st.markdown(res)
