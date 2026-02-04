import PyPDF2
from docx import Document
from pptx import Presentation
import io

class DocumentProcessor:
    @staticmethod
    def extract_text(uploaded_file):
        if not uploaded_file: return ""
        
        name = uploaded_file.name.lower()
        
        # 1. PDF Handler
        if name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() for page in reader.pages[:15]])
        
        # 2. Word Doc Handler
        elif name.endswith('.docx'):
            doc = Document(uploaded_file)
            return " ".join([para.text for para in doc.paragraphs])
        
        # 3. PowerPoint Handler
        elif name.endswith('.pptx'):
            prs = Presentation(uploaded_file)
            text_runs = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text_runs.append(shape.text)
            return " ".join(text_runs)
        
        # 4. Image Handler (Vision Trigger)
        elif name.endswith(('.png', '.jpg', '.jpeg')):
            return "[IMAGE_READY]"
        
        return "Unsupported format."
