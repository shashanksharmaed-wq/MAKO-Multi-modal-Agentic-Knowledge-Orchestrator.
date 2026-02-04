import google.generativeai as genai
import os
import streamlit as st

class APIHandler:
    def __init__(self):
        # 1. Fetch Key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key and "GOOGLE_API_KEY" in st.secrets:
            self.api_key = st.secrets["GOOGLE_API_KEY"]

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY missing from Secrets.")
        
        # 2. Initialize
        genai.configure(api_key=self.api_key)
        
        # 3. Model Selection (Using the specific 'latest' tag to avoid 404)
        # If 'gemini-1.5-pro-latest' fails, 'gemini-1.5-flash' is the safest backup
        try:
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        except Exception:
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def call_gemini(self, prompt):
        try:
            # Temperature 0.2: Logical, not creative.
            response = self.model.generate_content(
                prompt, 
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            # This helps us see the EXACT error in the UI
            return f"Council Communication Failure: {str(e)}"
