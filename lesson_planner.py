import streamlit as st
import os
from PIL import Image
from lesson_planner import LessonPlanner

# --- 1. INITIALIZE ARCHITECTURAL COMPONENTS ---
planner = LessonPlanner()

# --- 2. STREAMLIT CONFIG (MUST BE FIRST) ---
st.set_page_config(
    page_title="MAKO | Agentic Knowledge Orchestrator",
    page_icon="🦅",
    layout="wide"
)

# --- 3. STYLING & UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_index=True)

st.title("🦅 MAKO | Multi-Modal Agentic Hub")
st.subheader("Bunker Build: 1.5L+ PM Portfolio Edition")

# --- 4. SIDEBAR: THE CONTROL TOWER ---
with st.sidebar:
    st.header("⚙️ System Parameters")
    mode = st.selectbox("Select Mode", ["Knowledge Extraction", "Lesson Planner", "Assessment Engine"])
    
    if mode == "Lesson Planner":
        pedagogy = st.selectbox("Pedagogy Model", ["5E Model", "Bloom's Taxonomy", "Direct Instruction"])
        duration = st.slider("Lecture Duration (Mins)", 20, 90, 40)
    
    st.divider()
    st.info("Status: System Active | Mars in Scorpio Frequency")

# --- 5. CORE WORKFLOW ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input Source")
    uploaded_file = st.file_uploader("Snap or Upload Textbook/Notes", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Content", use_column_width=True)

with col2:
    st.header("🚀 Agentic Output")
    
    if st.button("EXECUTE STRIKE"):
        if uploaded_file:
            with st.spinner("MAKO is orchestrating..."):
                # --- MOCK LOGIC FOR AGENT RESPONSE ---
                # In your real code, replace this with your LLM/Vision call
                mock_response = {
                    "Introduction": "Core concepts identified from the image.",
                    "Detailed Plan": f"A {duration} minute lesson using {pedagogy}.",
                    "Assessment": "3 Quiz questions generated based on content."
                }
                
                # Display Results
                for section, text in mock_response.items():
                    st.write(f"**{section}**")
                    st.info(text)
                
                # --- PDF GENERATION ---
                if mode == "Lesson Planner":
                    pdf_filename = "MAKO_Lesson_Plan.pdf"
                    # Generate the PDF byte data
                    pdf_data = planner.generate_pdf(mock_response)
                    
                    st.success("Lesson Plan Compiled Successfully!")
                    st.download_button(
                        label="📥 Download PDF Lesson Plan",
                        data=pdf_data,
                        file_name=pdf_filename,
                        mime="application/pdf"
                    )
        else:
            st.warning("Please upload an image to trigger the agent.")

# --- 6. SYSTEM FOOTER ---
st.divider()
st.caption("MAKO v2.0 | God-Built for Institutional Deployment")
