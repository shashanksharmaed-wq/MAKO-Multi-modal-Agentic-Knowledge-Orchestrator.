import PyPDF2
import io

class DocumentProcessor:
    @staticmethod
    def extract_text(uploaded_file):
        if uploaded_file is None:
            return ""
        
        # Check if it's a PDF
        if uploaded_file.name.endswith('.pdf'):
            try:
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                # Read first 15 pages for context (to avoid token limits)
                for page in pdf_reader.pages[:15]:
                    text += page.extract_text()
                return text
            except Exception as e:
                return f"Error reading PDF: {e}"
        
        # If it's an Image (GPT-4o handles text description via prompt)
        else:
            return "Note: This is an image file. Analyzing visual content directly via Vision API."
