import PyPDF2

class DocumentProcessor:
    @staticmethod
    def extract_text(pdf_file):
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(reader.pages)
            
            # If the PDF is huge, we take the first 10 and last 5 pages 
            # to capture the "Context" and the "Conclusion".
            pages_to_read = list(range(min(10, total_pages)))
            if total_pages > 15:
                pages_to_read.extend(range(total_pages-5, total_pages))

            full_text = ""
            for i in pages_to_read:
                text = reader.pages[i].extract_text()
                if text:
                    full_text += text
            
            # THE SAFETY SLICE: Ensure we never exceed 25k tokens (~100k characters)
            return full_text[:100000] 
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
