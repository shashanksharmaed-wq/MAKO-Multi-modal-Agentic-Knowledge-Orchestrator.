import os

class Researcher:
    def __init__(self, model_type="gemini"):
        self.model_type = model_type

    def get_prompt(self, raw_text):
        return f"""
        ROLE: You are the 'Lead Researcher' in a 0.01% Agentic Council.
        TASK: Analyze the following educational material and extract the 5 most critical logical concepts.
        
        GUIDELINES:
        1. Do NOT summarize. Extract high-density logical structures.
        2. Identify potential 'Logic Fractures' where a student might get confused.
        3. Output your findings in a structured format for the 'Critic Agent' to review.
        
        MATERIAL:
        {raw_text}
        """
