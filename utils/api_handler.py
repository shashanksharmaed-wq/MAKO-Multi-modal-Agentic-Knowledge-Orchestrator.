import base64
from openai import OpenAI
import streamlit as st

class APIHandler:
    def __init__(self):
        # Ensure your secret key is 'OPENAI_API_KEY' in Streamlit Secrets
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def call_openai(self, prompt, image_file=None):
        try:
            if image_file:
                # Proper way to read Streamlit UploadedFile for Vision
                image_bytes = image_file.getvalue()
                b64 = base64.b64encode(image_bytes).decode('utf-8')
                content = [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            else:
                content = prompt

            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": content}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"Council Brain Error: {str(e)}"
