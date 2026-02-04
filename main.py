import streamlit as st
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher

# --- UI CONFIGURATION ---
st.set_page_config(page_title="MAKO | Agentic Knowledge Orchestrator", layout="wide")

# Custom CSS for the 1.0L+ Architect Look
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .thought-box { background-color: #161b22; border-left: 4px solid #58a6ff; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: 'Courier New', Courier, monospace; font-size: 0.9em; color: #8b949e; }
    .verdict-box { background-color: #21262d; border: 1px solid #30363d; padding: 20px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# --- SIDEBAR: INTERNAL MONOLOGUE ---
with st.sidebar:
    st.title("🦅 MAKO COUNCIL")
    st.status("System: Operational", state="complete")
    st.subheader("Internal Thought Process")
    thought_container = st.empty() 
    st.divider()
    st.info("MAKO is currently running on the OpenAI GPT-4o Backbone.")

# --- MAIN UI ---
st.title("Multi-Modal Agentic Knowledge Orchestrator")
st.write("Targeting **Pedagogical Remediation** & **Automated Audit**")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Step 1: Source Truth")
    source_pdf = st.file_uploader("Upload Textbook/Manual (PDF)", type="pdf")

with col2:
    st.subheader("📝 Step 2: Ingest Failure")
    answer_sheet = st.file_uploader("Upload Student Work (Image/PDF)", type=["pdf", "jpg", "jpeg", "png"])

st.divider()

# --- ACTION BUTTONS ---
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("🚀 Run Diagnostic Audit", use_container_width=True):
        if source_pdf and answer_sheet:
            with st.spinner("Council is deliberating..."):
                # 1. Process Files
                context = DocumentProcessor.extract_text(source_pdf)
                student_work = DocumentProcessor.extract_text(answer_sheet)
                
                # 2. Researcher Agent Action
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Mapping student failure points to source context...</div>", unsafe_allow_html=True)
                agent = Researcher(st.session_state.handler)
                report = agent.analyze(context, student_work)
                
                st.session_state.final_report = report
                thought_container.markdown("<div class='thought-box'>[COUNCIL]: Logic gaps identified. Report generated.</div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload both the Source and the Student Work.")

with btn_col2:
    if st.button("📚 Generate High-Yield Notes", use_container_width=True):
        if source_pdf:
            with st.spinner("Distilling knowledge..."):
                context = DocumentProcessor.extract_text(source_pdf)
                agent = Researcher(st.session_state.handler)
                notes = agent.generate_notes(context)
                st.session_state.final_report = notes
                thought_container.markdown("<div class='thought-box'>[RESEARCHER]: Distilling PDF into conceptual pillars...</div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload the Source PDF first.")

# --- DISPLAY RESULTS ---
if "final_report" in st.session_state:
    st.markdown("<div class='verdict-box'>", unsafe_allow_html=True)
    st.markdown(st.session_state.final_report)
    st.markdown("</div>", unsafe_allow_html=True)
