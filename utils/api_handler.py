import google.generativeai as genai
import os
import streamlit as st

class APIHandler:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key and "GOOGLE_API_KEY" in st.secrets:
            self.api_key = st.secrets["GOOGLE_API_KEY"]
        
        genai.configure(api_key=self.api_key)

    def get_available_models(self):
        """Returns a list of all models your API key can actually use."""
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models

    def call_gemini(self, prompt):
        # We will use this to find the right name
        available = self.get_available_models()
        # Standard fallback logic
        model_name = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available else available[0]
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Available Models: {available} | Error: {str(e)}"
