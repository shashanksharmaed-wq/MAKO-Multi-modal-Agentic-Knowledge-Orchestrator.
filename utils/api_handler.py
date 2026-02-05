import base64
from openai import OpenAI
import streamlit as st

class APIHandler:
    def __init__(self):
        # Using Streamlit Secrets for the 1.0L+ professional deployment
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def call_openai(self, prompt, image_file=None):
        try:
            if image_file:
                # Convert the uploaded file to Base64 for GPT-4o Vision
                image_bytes = image_file.getvalue() # Use getvalue() for Streamlit files
                b64 = base64.b64encode(image_bytes).decode('utf-8')
                
                content = [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url", 
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    }
                ]
            else:
                content = prompt

            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": content}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Council Logic Failure: {str(e)}"
