import streamlit as st
from utils.api_handler import APIHandler
from utils.document_processor import DocumentProcessor
from agents.researcher import Researcher

st.set_page_config(page_title="MAKO | Agentic Hub", layout="wide")

# Initialize Brain
if "handler" not in st.session_state:
    st.session_state.handler = APIHandler()

# --- SIDEBAR: MISSION SELECTION ---
with st.sidebar:
    st.title("🦅 MAKO Console")
    # THE PIVOT: Give the user choices so it's always practical
    mode = st.radio("Select Council Task:", 
                    ["📚 Note Generator", "✍️ Mock Test Creator", "⚖️ Surgical Auditor"])
    st.divider()
    st.info(f"Mode: {mode}")

st.title("Multi-Modal Knowledge Orchestrator")

# STEP 1: UPLOAD SOURCE (Required for all modes)
st.subheader("Step 1: Upload Source Truth")
source_pdf = st.file_uploader("Upload Textbook / Manual (PDF)", type="pdf")

st.divider()

# STEP 2: DYNAMIC INPUTS BASED ON MODE
st.subheader(f"Step 2: {mode} Configuration")

if mode == "📚 Note Generator":
    st.write("The Council will distill the PDF into high-yield revision notes.")
    topic_focus = st.text_input("Specific topic? (Leave blank for full summary)")

elif mode == "✍️ Mock Test Creator":
    st.write("Generate a custom exam based on the PDF content.")
    num_q = st.slider("Number of Questions", 5, 20, 10)

elif mode == "⚖️ Surgical Auditor":
    st.write("Upload a specific complex answer to verify against the source.")
    student_work = st.text_area("Paste the Student's Answer or Doubt here...")

# STEP 3: EXECUTION
if st.button(f"🚀 Execute {mode}"):
    if source_pdf:
        with st.spinner("The Council is deliberating..."):
            context = DocumentProcessor.extract_text(source_pdf)
            agent = Researcher(st.session_state.handler)
            
            if mode == "📚 Note Generator":
                output = agent.generate_notes(context, topic_focus)
            elif mode == "✍️ Mock Test Creator":
                output = agent.generate_test(context, num_q)
            elif mode == "⚖️ Surgical Auditor":
                output = agent.analyze(context, student_work)
            
            st.session_state.final_output = output
    else:
        st.error("Please upload the Source PDF first.")

# STEP 4: DISPLAY RESULTS
if "final_output" in st.session_state:
    st.divider()
    st.subheader("📋 Council Result")
    st.markdown(st.session_state.final_output)
    st.download_button("📥 Download Report", st.session_state.final_output, file_name=f"MAKO_{mode}.txt")
