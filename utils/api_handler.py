import google.generativeai as genai
import os
import streamlit as st

class APIHandler:
    def __init__(self):
        # 1. Fetch the NEW Key from Secrets
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key and "GOOGLE_API_KEY" in st.secrets:
            self.api_key = st.secrets["GOOGLE_API_KEY"]

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY missing from Secrets. Please rotate your leaked key.")
        
        # 2. Configure
        genai.configure(api_key=self.api_key)
        
        # 3. Model Selection: Using the Elite 2.5 Pro
        # This model has superior agentic reasoning.
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def call_gemini(self, prompt):
        try:
            # Temperature 0.2: Logical precision (The Panna Frequency)
            response = self.model.generate_content(
                prompt, 
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            # If 2.5 Pro has a regional limit, fallback to 2.5 Flash
            if "403" in str(e) or "429" in str(e):
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                return self.call_gemini(prompt)
            return f"Council Communication Failure: {str(e)}"
