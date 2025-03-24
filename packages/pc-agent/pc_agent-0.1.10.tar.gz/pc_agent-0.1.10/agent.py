class Agent:
    def __init__(self, system_instruction: str, model_name: str, goal: str):
        self.system_instruction = system_instruction
        self.model_name = model_name 
        self.goal = goal
        self._history = []
        self._response = None

    def run(self, user_input: str):
        response = self._get_response(user_input)
        self._history.append({
            'user_input': user_input,
            'response': response
        })
        self._response = response
        return response

    def _get_response(self, user_input: str):
        # In a real implementation, this would call the LLM API
        # For now, we'll return a simple response for testing

        return f"Processed: {user_input}"