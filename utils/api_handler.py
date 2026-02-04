import os
import base64
import streamlit as st
from openai import OpenAI

class APIHandler:
    def __init__(self):
        self.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def call_gemini(self, prompt, image_file=None):
        try:
            # VISION PATH: If an image is provided
            if image_file and not image_file.name.endswith(('.pdf', '.docx')):
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }]
                )
            # TEXT PATH: For PDF or Word
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
            return response.choices[0].message.content
        except Exception as e:
            return f"Council Communication Failure: {str(e)}"
