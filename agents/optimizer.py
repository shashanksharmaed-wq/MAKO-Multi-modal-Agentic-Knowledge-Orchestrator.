class Optimizer:
    def __init__(self, model_type="gemini"):
        self.model_type = model_type

    def get_prompt(self, researcher_output, critic_feedback):
        return f"""
        ROLE: You are the 'Lead Optimizer' in a 0.01% Agentic Council. 
        Your job is to resolve the debate between the Researcher and the Critic.

        TASK: Produce a final, flawless Pedagogical Assessment.
        
        INPUT DATA:
        - Original Research: {researcher_output}
        - Critic's Objections: {critic_feedback}

        INSTRUCTIONS:
        1. Address every single 'FLAW' mentioned by the Critic.
        2. Ensure the tone is professional and suitable for a 1.0L+ EdTech environment.
        3. Format the final output into a clear quiz/assessment structure.
        4. Do NOT include any meta-talk about the agents. Just provide the perfect result.
        """
