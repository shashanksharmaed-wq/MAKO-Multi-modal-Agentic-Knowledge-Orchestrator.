import PyPDF2
from docx import Document
import io

class DocumentProcessor:
    @staticmethod
    def extract_text(uploaded_file):
        if not uploaded_file: return ""
        
        name = uploaded_file.name.lower()
        
        # PDF Handler
        if name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() for page in reader.pages[:15]])
        
        # Word Doc Handler
        elif name.endswith('.docx'):
            doc = Document(uploaded_file)
            return " ".join([para.text for para in doc.paragraphs])
        
        # Image Handler (We return a flag so the API knows to use Vision)
        elif name.endswith(('.png', '.jpg', '.jpeg')):
            return "[IMAGE_UPLOADED]"
        
        return "Unsupported format."
