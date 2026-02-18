import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import io

class LessonPlanner:
    def __init__(self):
        # Define the 5 pedagogical models
        self.pedagogies = {
            "Direct Instruction": "Focus on explicit teaching: I Do, We Do, You Do.",
            "Inquiry-Based": "Focus on exploration: Trigger curiosity with a central question.",
            "5E Model": "Engage, Explore, Explain, Elaborate, Evaluate.",
            "BOPPPS": "Bridge-in, Objective, Pre-test, Participatory, Post-test, Summary.",
            "Flipped Classroom": "Pre-class content (video/reading) followed by in-class application."
        }

    def extract_text(self, uploaded_file):
        """Extracts text from scanned images or PDF pages."""
        try:
            if uploaded_file.type == "application/pdf":
                images = convert_from_bytes(uploaded_file.read())
                text = ""
                for img in images:
                    text += pytesseract.image_to_string(img)
            else:
                image = Image.open(uploaded_file)
                text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            return f"Error reading document: {str(e)}"

    def render_ui(self):
        st.subheader("🍎 Lesson Architect")
        st.markdown("Scan your source material (textbook page, handwritten notes, or PDF) to generate a plan.")

        col1, col2 = st.columns([1, 1])
        with col1:
            uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'png', 'jpg', 'jpeg'])
            pedagogy = st.selectbox("Choose Pedagogy", list(self.pedagogies.keys()))
        
        with col2:
            st.info(f"**Strategy Note:** {self.pedagogies[pedagogy]}")

        if uploaded_file and st.button("Generate Descriptive Plan"):
            with st.spinner("Analyzing content and orchestrating pedagogy..."):
                extracted_text = self.extract_text(uploaded_file)
                
                if extracted_text.strip():
                    st.success("Document Scanned Successfully!")
                    # Here you would typically send 'extracted_text' and 'pedagogy' to an LLM
                    # For now, we display the extraction and the plan structure
                    st.markdown("---")
                    st.markdown(f"### 📝 Generated {pedagogy} Lesson Plan")
                    st.write("**Learning Objective:** Derived from scanned content.")
                    st.write("**Sequence:** Logic based on " + pedagogy)
                    st.text_area("Scanned Content Reference", extracted_text, height=150)
                else:
                    st.error("Could not extract text. Please ensure the scan is clear.")
