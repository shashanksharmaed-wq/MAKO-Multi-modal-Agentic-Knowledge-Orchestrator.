import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class APIHandler:
    def __init__(self):
        # This looks for your API key in the environment
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def call_gemini(self, prompt):
        try:
            # Temperature 0.2 is the 'Logic' setting for Mercury/Panna frequency
            response = self.model.generate_content(
                prompt, 
                generation_config={"temperature": 0.2}
            )
            return response.text
        except Exception as e:
            return f"Council Communication Failure: {str(e)}"
