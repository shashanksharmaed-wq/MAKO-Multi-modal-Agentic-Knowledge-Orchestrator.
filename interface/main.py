import streamlit as st
from agents.researcher import Researcher
from agents.critic import Critic
from agents.optimizer import Optimizer
from utils.api_handler import APIHandler # We will build this next

st.set_page_config(page_title="MAKO Evaluator", page_icon="🦅")

st.title("🦅 MAKO: Agentic Council")
st.markdown("---")

# Initialize Agents and Handler
handler = APIHandler()
researcher = Researcher()
critic = Critic()
optimizer = Optimizer()

uploaded_file = st.file_uploader("Upload Material", type="pdf")

if uploaded_file:
    # Logic to extract text from PDF would go here
    raw_text = "Sample extracted text from student material..." 
    
    if st.button("Activate Council"):
        # STEP 1: Research
        with st.status("Agent 1: Researching...", state="running"):
            research_data = handler.call_gemini(researcher.get_prompt(raw_text))
            st.write("✅ Research Complete")
        
        # STEP 2: Critique
        with st.status("Agent 2: Finding Logic Fractures...", state="running"):
            critic_feedback = handler.call_gemini(critic.get_prompt(research_data))
            st.write("✅ Critique Logged")
            st.info(f"Critic Status: {critic_feedback[:200]}...") # Show a snippet

        # STEP 3: Optimize
        with st.status("Agent 3: Finalizing Assessment...", state="running"):
            final_output = handler.call_gemini(optimizer.get_prompt(research_data, critic_feedback))
            st.success("🎯 Assessment Perfected!")

        st.subheader("The Final 0.01% Output")
        st.write(final_output)
