import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from .env for local development
load_dotenv()

class APIHandler:
    def __init__(self):
        """
        Initializes the Gemini 1.5 Pro connection.
        It prioritizes the 'GOOGLE_API_KEY' found in environment variables 
        (Secrets in Streamlit Cloud or .env locally).
        """
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            # This will show up in your Streamlit logs if the Secret is missing
            raise ValueError("GOOGLE_API_KEY not found. Please set it in Streamlit Secrets or .env file.")
        
        # Configure the Google Generative AI library
        genai.configure(api_key=self.api_key)
        
        # Selecting the Pro model for 0.01% reasoning capabilities
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def call_gemini(self, prompt):
        """
        Sends a prompt to the Council's brain and returns the logical response.
        """
        try:
            # Temperature 0.2: The 'Panna' frequency (Cold, Precise, Logical)
            response = self.model.generate_content(
                prompt, 
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            return f"Council Communication Failure: {str(e)}"
