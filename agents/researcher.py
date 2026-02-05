class Researcher:
    def __init__(self, handler):
        self.handler = handler

    # FIX: Added 'img' parameter to match the call in main.py
    def generate_test(self, context, img=None):
        prompt = f"""
        TASK: Generate a 10-question Mock Test based on the provided source.
        SOURCE TEXT: {context[:30000]}
        INSTRUCTION: If an image is provided, analyze the visual diagrams/text to create questions.
        FORMAT: MCQ with an Answer Key at the end.
        """
        # Ensure your handler is called correctly
        return self.handler.call_openai(prompt, img)

    def generate_notes(self, context, img=None):
        prompt = f"Create high-yield notes from this source: {context[:30000]}"
        return self.handler.call_openai(prompt, img)

    def analyze(self, source, evidence, s_img=None, e_img=None):
        prompt = f"AUDIT: Compare {evidence} against {source}."
        return self.handler.call_openai(prompt, e_img if e_img else s_img)
