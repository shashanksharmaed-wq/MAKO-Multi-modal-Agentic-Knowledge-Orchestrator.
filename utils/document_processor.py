import PyPDF2

class DocumentProcessor:
    @staticmethod
    def extract_text(pdf_file):
        """Extracts text from an uploaded PDF file."""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text
            return full_text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
