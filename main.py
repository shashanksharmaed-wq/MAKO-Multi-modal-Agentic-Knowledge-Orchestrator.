import subprocess
import sys
import streamlit as st

# --- THE 0.01% FORCE INSTALL ---
try:
    import openai
except ImportError:
    st.warning("🛠️ Environment incomplete. Force-installing 'openai'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    st.rerun()

# ... rest of your imports (Researcher, APIHandler, etc.)import streamlit as st
from agents.researcher import Researcher
from agents.critic import Critic
from agents.optimizer import Optimizer
from agents.remedial_architect import RemedialArchitect
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor

st.set_page_config(page_title="MAKO Agentic Engine", page_icon="🦅", layout="wide")

# --- UI Header ---
st.title("🦅 MAKO: Agentic Knowledge Orchestrator")
st.info("Status: Bunker Build | 0.01% Recursive Evaluation Mode")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Engine Settings")
    model_choice = st.selectbox("Intelligence Core", ["Gemini 1.5 Pro", "GPT-4o (Soon)"])
    st.divider()
    st.markdown("### The Council Status")
    st.write("🕵️ Researcher: **Online**")
    st.write("⚖️ Critic: **Online**")
    st.write("🛠️ Optimizer: **Online**")
    st.write("🎯 Remedial Architect: **Online**")

# --- Main Logic ---
handler = APIHandler()
doc_tool = DocumentProcessor()

uploaded_file = st.file_uploader("Upload Pedagogical Material (PDF)", type="pdf")

if uploaded_file:
    # 1. READ
    with st.spinner("Ingesting material..."):
        raw_text = doc_tool.extract_text(uploaded_file)
    st.success("Material Verified. Ready to Strike.")

    if st.button("🚀 ACTIVATE AGENTIC COUNCIL"):
        # Create Layout Columns for the Council Debate
        c1, c2 = st.columns(2)
        
        # STEP 1: RESEARCH
        with c1:
            with st.expander("🕵️ Agent 1: Research Log", expanded=True):
                research_data = handler.call_gemini(Researcher().get_prompt(raw_text))
                st.write(research_data)

        # STEP 2: CRITIQUE
        with c2:
            with st.expander("⚖️ Agent 2: Logic Audit", expanded=True):
                critic_feedback = handler.call_gemini(Critic().get_prompt(research_data))
                st.write(critic_feedback)

        st.divider()

        # STEP 3 & 4: THE PRODUCT
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.subheader("🎯 Optimized Assessment")
            with st.spinner("Agent 3: Finalizing..."):
                final_output = handler.call_gemini(Optimizer().get_prompt(research_data, critic_feedback))
                st.write(final_output)

        with col_res2:
            st.subheader("🗓️ Remedial Execution Blueprint")
            with st.spinner("Agent 4: Architecting..."):
                remedial_plan = handler.call_gemini(RemedialArchitect().get_prompt(critic_feedback, raw_text))
                st.markdown(remedial_plan)

        st.balloons() # The 1.0L+ Victory signal
