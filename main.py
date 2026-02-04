import streamlit as st
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher
# Import other agents as you create them (Critic, Optimizer)

# --- UI CONFIGURATION (The 1.0L+ Aesthetic) ---
st.set_page_config(page_title="MAKO | Agentic Orchestrator", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #0e1117; color: white; }
    .stSidebar { background-color: #161b22; border-right: 1px solid #30363d; }
    .thought-box { background-color: #0d1117; border-left: 3px solid #58a6ff; padding: 10px; margin: 10px 0; font-style: italic; color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: THE INTERNAL MONOLOGUE ---
with st.sidebar:
    st.title("🦅 MAKO Council")
    st.info("The Council is currently monitoring the environment.")
    st.subheader("Internal Thought Process")
    thought_container = st.empty() # This is where the 'Debate' will show up

# --- MAIN INTERFACE ---
st.title("Multi-Modal Agentic Knowledge Orchestrator")
st.caption("Pedagogical Remediation Engine | 0.01% Architect Tier")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Step 1: Ingest Truth (PDF)")
    uploaded_file = st.file_uploader("Upload Pedagogical Material", type="pdf")

with col2:
    st.subheader("Step 2: Input Failure (Answer Sheet)")
    student_input = st.text_area("Paste Student Answers or Mistakes here...", height=150)

if st.button("🚀 Ignite the Council"):
    if uploaded_file and student_input:
        with st.spinner("Council is deliberating..."):
            # 1. Process Document
            context = DocumentProcessor.extract_text(uploaded_file)
            
            # 2. Researcher Agent (The First Chair)
            thought_container.markdown("<div class='thought-box'>Researcher: Scanning PDF for conceptual anchors...</div>", unsafe_allow_html=True)
            researcher = Researcher(st.session_state.handler)
            research_report = researcher.analyze(context, student_input)
            
            # Display Results
            st.divider()
            st.subheader("📋 The Council's Verdict")
            st.markdown(research_report)
            
            # (Optional) You can add Critic and Optimizer here following the same pattern
            thought_container.markdown("<div class='thought-box'>Council: Deliberation Complete. Remediation path generated.</div>", unsafe_allow_html=True)
    else:
        st.warning("Please provide both the PDF and the Student Input.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write(f"**Status:** Operational")
st.sidebar.write(f"**Model:** GPT-4o (OpenAI)")
