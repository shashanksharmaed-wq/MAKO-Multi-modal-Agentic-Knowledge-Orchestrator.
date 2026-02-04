class Researcher:
    def __init__(self, handler):
        self.handler = handler

    def analyze(self, context, student_work):
        prompt = f"""
        ROLE: Senior Pedagogical Auditor.
        TASK: Compare the STUDENT WORK against the SOURCE TRUTH.
        
        SOURCE TRUTH: {context[:40000]}
        STUDENT WORK: {student_work[:10000]}
        
        GOAL: Identify the specific logical failures in the student's understanding. 
        For every error, cite the page/section from the source.
        """
        return self.handler.call_gemini(prompt)

    def generate_notes(self, context):
        prompt = f"""
        ROLE: Master Educator.
        TASK: Create high-yield revision notes from the provided text.
        
        CONTEXT: {context[:40000]}
        
        FORMAT: 
        - Use Bold headers.
        - Use Bullet points for key definitions.
        - Add a 'Common Pitfalls' section.
        """
        return self.handler.call_gemini(prompt)
