import streamlit as st
import os
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher

# --- 1. UI CONFIGURATION (0.01% Architect Aesthetic) ---
st.set_page_config(
    page_title="MAKO | Universal Agentic Hub",
    page_icon="🦅",
    layout="wide"
)

# Custom CSS for a professional "Dark Mode" console look
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stSidebar { background-color: #161b22; border-right: 1px solid #30363d; }
    .thought-box { 
        background-color: #010409; 
        border-left: 4px solid #58a6ff; 
        padding: 12px; 
        border-radius: 4px; 
        font-family: 'Courier New', monospace; 
        font-size: 0.85em; 
        color: #8b949e;
        margin-bottom: 10px;
    }
    .result-container {
        background-color: #161b22;
        padding: 25px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# --- 3. SIDEBAR: THE COUNCIL CONTROL ---
with st.sidebar:
    st.title("🦅 MAKO COUNCIL")
    st.markdown("---")
    
    # Mode Selection: The Swiss Army Knife approach
    mode = st.radio(
        "Select Operation Mode:",
        ["📚 Notes Generator", "✍️ Mock Test Creator", "⚖️ Diagnostic Auditor"],
        help="Choose the specific logic for the Council to follow."
    )
    
    st.markdown("---")
    st.subheader("Internal Thought Process")
    thought_container = st.empty() # Dynamic placeholder for the 'Council Debate'
    
    if st.button("🧹 Clear Workspace"):
        st.session_state.clear()
        st.rerun()

# --- 4. MAIN INTERFACE ---
st.title("Multi-Modal Agentic Knowledge Orchestrator")
st.caption("Universal Ingestion Engine: PDF | DOCX | PPTX | VISION")

# DUAL INGESTION COLS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Step 1: Ingest Truth")
    # Universal file uploader
    source_file = st.file_uploader(
        "Upload Source (Textbook, PPT, or Photo)", 
        type=["pdf", "docx", "pptx", "jpg", "jpeg", "png"],
        key="main_source"
    )

with col2:
    if mode == "⚖️ Diagnostic Auditor":
        st.subheader("📝 Step 2: Ingest Failure")
        evidence_file = st.file_uploader(
            "Upload Student Work (Image/PDF)", 
            type=["pdf", "docx", "jpg", "jpeg", "png"],
            key="audit_evidence"
        )
    else:
        st.subheader("🎯 Step 2: Focus")
        focus_topic = st.text_input("Focus on a specific topic? (Optional)", placeholder="e.g. Calvin Cycle, Calculus, etc.")

st.divider()

# --- 5. EXECUTION LOGIC ---
if st.button(f"🚀 Execute {mode}", use_container_width=True):
    if source_file:
        with st.spinner("The Council is deliberating..."):
            # A. Extract Source Text/Vision Flag
            source_content = DocumentProcessor.extract_text(source_file)
            is_source_img = "[IMAGE_READY]" in source_content
            
            # B. Initialize Agent
            agent = Researcher(st.session_state.handler)
            
            # C. Execute based on Mode
            if mode == "📚 Notes Generator":
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Distilling foundational concepts from source...</div>", unsafe_allow_html=True)
                res = agent.generate_notes(source_content, source_file if is_source_img else None)
            
            elif mode == "✍️ Mock Test Creator":
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Analyzing document structure to generate evaluation logic...</div>", unsafe_allow_html=True)
                res = agent.generate_test(source_content, source_file if is_source_img else None)
            
            elif mode == "⚖️ Diagnostic Auditor":
                if evidence_file:
                    evidence_content = DocumentProcessor.extract_text(evidence_file)
                    is_evidence_img = "[IMAGE_READY]" in evidence_content
                    
                    thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Mapping student work against primary source truth...</div>", unsafe_allow_html=True)
                    res = agent.analyze(
                        source_content, 
                        evidence_content, 
                        source_file if is_source_img else None,
                        evidence_file if is_evidence_img else None
                    )
                else:
                    st.error("Audit mode requires student evidence (Answer Sheet).")
                    st.stop()
            
            # D. Finalize
            st.session_state.final_output = res
            thought_container.markdown("<div class='thought-box'>[COUNCIL]: Analysis complete. Report finalized.</div>", unsafe_allow_html=True)
    else:
        st.error("Please upload a source file to begin.")

# --- 6. RESULTS DISPLAY ---
if "final_output" in st.session_state:
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    st.markdown(st.session_state.final_output)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download functionality
    st.download_button(
        label="📥 Download Report",
        data=st.session_state.final_output,
        file_name=f"MAKO_{mode.replace(' ', '_')}.md",
        mime="text/markdown"
    )
