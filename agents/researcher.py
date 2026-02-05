class Researcher:
    def __init__(self, handler):
        self.handler = handler

    def generate_notes(self, context, img=None, topic=""):
        prompt = f"Create high-yield revision notes for {topic}. Source Truth: {context[:30000]}"
        return self.handler.call_openai(prompt, img)

    def generate_test(self, context, img=None):
        prompt = f"Generate a 10-question MCQ Mock Test with an Answer Key based on this source: {context[:30000]}"
        return self.handler.call_openai(prompt, img)

    def analyze(self, source, evidence, s_img=None, e_img=None):
        prompt = f"AUDIT: Compare student evidence against source truth. Identify errors.\nSource: {source[:20000]}\nEvidence: {evidence[:10000]}"
        # Prioritize evidence image for vision if available
        return self.handler.call_openai(prompt, e_img if e_img else s_img)
