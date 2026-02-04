class Researcher:
    def __init__(self, handler):
        self.handler = handler

    def generate_notes(self, context, topic=""):
        target = f"focusing on {topic}" if topic else "the entire document"
        prompt = f"Create structured, high-yield revision notes {target} using this source: {context[:40000]}"
        return self.handler.call_gemini(prompt)

    def generate_test(self, context, count):
        prompt = f"Create {count} multiple-choice questions (MCQs) with an answer key based on: {context[:40000]}"
        return self.handler.call_gemini(prompt)

    def analyze(self, context, student_work):
        prompt = f"Compare this student answer to the source and identify logical errors: \nSource: {context[:40000]}\nAnswer: {student_work}"
        return self.handler.call_gemini(prompt)
