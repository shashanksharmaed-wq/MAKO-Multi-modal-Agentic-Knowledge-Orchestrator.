from fpdf import FPDF

class LessonPlanner:
    def __init__(self):
        # Define the Pedagogy Blueprints
        self.pedagogies = {
            "5E": "Engage, Explore, Explain, Elaborate, Evaluate",
            "Bloom": "Remember, Understand, Apply, Analyze, Evaluate, Create",
            "Direct": "Intro, Modeling (I Do), Guided (We Do), Independent (You Do), Closure"
        }

    def generate_pdf(self, content_json, filename="Lesson_Plan.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Header
        pdf.cell(200, 10, txt="MAKO | Automated Lesson Plan", ln=True, align='C')
        pdf.ln(10)
        
        # Mapping Content to PDF
        pdf.set_font("Arial", size=12)
        for section, detail in content_json.items():
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=section.upper(), ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, txt=detail)
            pdf.ln(5)
            
        pdf.output(filename)
        return filename

    def get_prompt_extension(self, pedagogy_type, time_duration):
        template = self.pedagogies.get(pedagogy_type, "Standard")
        return f"\n\nACT AS: Senior Instructional Designer. \nTASK: Create a {time_duration} minute lesson plan using the {pedagogy_type} model ({template}). \nOUTPUT: Return a JSON with these phases as keys."
