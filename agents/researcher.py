class Researcher:
    def __init__(self, handler):
        self.handler = handler

    def analyze(self, context, evidence, evidence_file=None):
        prompt = f"AUDIT TASK: Use Source Truth to verify Student Evidence.\nTRUTH: {context[:30000]}\nEVIDENCE: {evidence}"
        return self.handler.call_gemini(prompt, image_file=evidence_file)

    def generate_notes(self, context, source_file=None):
        prompt = f"MAKER TASK: Distill this source into high-yield revision notes. \nSOURCE: {context[:40000]}"
        return self.handler.call_gemini(prompt, image_file=source_file)
