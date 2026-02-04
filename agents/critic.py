class Critic:
    def __init__(self, model_type="gemini"):
        self.model_type = model_type

    def get_prompt(self, researcher_output):
        return f"""
        ROLE: You are the 'Lead Critic' in a 0.01% Agentic Council. 
        Your job is to find flaws, hallucinations, and logic fractures in the Researcher's work.

        TASK: Critically evaluate the following research summary.
        
        SKEPTICISM GUIDELINES:
        1. Is there any 'Hallucination'? (Did the AI add facts not in the original text?)
        2. Is the pedagogical logic sound? If a student follows this, will they be confused?
        3. Identify 'Vague Areas' that need more detail.
        4. Be harsh. If the quality is not 10/10, demand a rewrite.

        RESEARCHER'S OUTPUT TO EVALUATE:
        {researcher_output}

        OUTPUT FORMAT:
        - STATUS: [PASS/FAIL]
        - FLAW_LIST: [List specific logical errors found]
        - RECOMMENDATIONS: [How to fix these for the Optimizer]
        """
