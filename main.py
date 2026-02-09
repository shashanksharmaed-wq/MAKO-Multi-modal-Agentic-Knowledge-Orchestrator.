import streamlit as st
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher

st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# Session Check
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# SIDEBAR
with st.sidebar:
    st.title("🦅 MAKO COUNCIL")
    mode = st.radio("Task Selection:", ["📚 Notes", "✍️ Mock Test", "⚖️ Audit"])
    if st.button("🧹 Reset System"):
        st.session_state.clear()
        st.rerun()

st.title("Multi-Modal Agentic Knowledge Orchestrator")

col1, col2 = st.columns(2)
with col1:
    source_file = st.file_uploader("Upload Source Truth", type=["pdf", "docx", "pptx", "jpg", "jpeg", "png"])
with col2:
    if mode == "⚖️ Audit":
        evidence_file = st.file_uploader("Upload Student Work", type=["pdf", "docx", "pptx", "jpg", "jpeg", "png"])
    else:
        topic = st.text_input("Topic Focus (Optional)")

if st.button(f"🚀 Execute {mode}", use_container_width=True):
    if source_file:
        with st.spinner("Council is deliberating..."):
            source_raw = DocumentProcessor.extract_text(source_file)
            is_source_img = "[IMAGE_READY]" in source_raw
            agent = Researcher(st.session_state.handler)
            
            if mode == "📚 Notes":
                res = agent.generate_notes(source_raw, source_file if is_source_img else None, topic if 'topic' in locals() else "")
            elif mode == "✍️ Mock Test":
                # This is the line that was failing - it is now fixed
                res = agent.generate_test(source_raw, source_file if is_source_img else None)
            elif mode == "⚖️ Audit":
                evid_raw = DocumentProcessor.extract_text(evidence_file)
                is_evid_img = "[IMAGE_READY]" in evid_raw
                res = agent.analyze(source_raw, evid_raw, source_file if is_source_img else None, evidence_file if is_evid_img else None)
            
            st.session_state.final_output = res
    else:
        st.error("Please upload a source file.")

if "final_output" in st.session_state:
    st.divider()
    st.markdown(st.session_state.final_output)
