import streamlit as st
import os

# --- 1. SAFE IMPORTS (Prevents NameError) ---
try:
    from utils.api_handler import APIHandler
    from utils.document_processor import DocumentProcessor
    from agents.researcher import Researcher
except ImportError as e:
    st.error(f"🚨 Path Error: {e}. Check if 'agents' and 'utils' folders are correct.")
    st.stop()

# --- 2. CONFIG & UI ---
st.set_page_config(page_title="MAKO | Agentic Hub", page_icon="🦅", layout="wide")

# Custom CSS for the 0.01% Architect Look
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .thought-box { background-color: #161b22; border-left: 4px solid #58a6ff; padding: 15px; font-family: monospace; color: #8b949e; }
    .result-container { background-color: #161b22; padding: 25px; border-radius: 10px; border: 1px solid #30363d; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. INITIALIZATION ---
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🦅 MAKO COUNCIL")
    st.divider()
    mode = st.radio("Task Selection:", ["📚 Notes", "✍️ Mock Test", "⚖️ Audit"])
    st.divider()
    thought_container = st.empty()
    if st.button("🧹 Reset Workspace"):
        st.session_state.clear()
        st.rerun()

# --- 5. MAIN INTERFACE ---
st.title("Multi-Modal Agentic Knowledge Orchestrator")
st.caption("Universal Engine: PDF | DOCX | PPTX | Vision (JPG/PNG)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📁 Step 1: Source Truth")
    source_file = st.file_uploader("Upload Textbook/Notes", type=["pdf", "docx", "pptx", "jpg", "jpeg", "png"])

with col2:
    if mode == "⚖️ Audit":
        st.subheader("📝 Step 2: Student Work")
        evidence_file = st.file_uploader("Upload Answer Sheet", type=["pdf", "docx", "pptx", "jpg", "jpeg", "png"])
    else:
        st.subheader("🎯 Step 2: Focus Area")
        focus_topic = st.text_input("Enter specific topic (Optional)")

# --- 6. EXECUTION ---
if st.button(f"🚀 Run {mode}", use_container_width=True):
    if source_file:
        with st.spinner("Council Deliberating..."):
            # A. Extract Source Text/Vision Flag
            source_raw = DocumentProcessor.extract_text(source_file)
            is_source_img = "[IMAGE_READY]" in source_raw
            
            # B. Initialize Agent
            agent = Researcher(st.session_state.handler)
            
            # C. Logic Mapping
            if mode == "📚 Notes":
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Distilling high-yield nodes...</div>", unsafe_allow_html=True)
                res = agent.generate_notes(source_raw, source_file if is_source_img else None)
            elif mode == "✍️ Mock Test":
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Generating evaluation logic...</div>", unsafe_allow_html=True)
                res = agent.generate_test(source_raw, source_file if is_source_img else None)
            elif mode == "⚖️ Audit":
                if evidence_file:
                    evidence_raw = DocumentProcessor.extract_text(evidence_file)
                    is_evid_img = "[IMAGE_READY]" in evidence_raw
                    thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Mapping evidence vs source...</div>", unsafe_allow_html=True)
                    res = agent.analyze(source_raw, evidence_raw, source_file if is_source_img else None, evidence_file if is_evid_img else None)
                else:
                    st.error("Audit requires student work.")
                    st.stop()
            
            st.session_state.final_output = res
    else:
        st.error("Source file required.")

# --- 7. DISPLAY RESULTS ---
if "final_output" in st.session_state:
    st.divider()
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.markdown(st.session_state.final_output)
    st.markdown("</div>", unsafe_allow_html=True)
    st.download_button("📥 Download Report", st.session_state.final_output, file_name=f"MAKO_{mode}.md")
