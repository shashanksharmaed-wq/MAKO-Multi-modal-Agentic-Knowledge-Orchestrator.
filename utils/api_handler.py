import os
import streamlit as st
from openai import OpenAI

class APIHandler:
    def __init__(self):
        # 1. Fetch OpenAI Key from Secrets
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key and "OPENAI_API_KEY" in st.secrets:
            self.api_key = st.secrets["OPENAI_API_KEY"]

        if not self.api_key:
            st.error("🔑 OpenAI API Key Missing in Streamlit Secrets!")
            st.stop()
        
        # 2. Initialize OpenAI Client
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = "gpt-4o" # Using the high-reasoning '4o' model

    def call_gemini(self, prompt): # We keep the method name same so main.py doesn't break
        try:
            # Temperature 0.2: Logical precision (The Panna Frequency)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Council Communication Failure: {str(e)}"
