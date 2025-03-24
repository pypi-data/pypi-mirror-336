from llms.llm import LLM
from typing import Optional, List, Dict, Any

class Agent:
    def __init__(self, system_instruction: str, llm: LLM, goal: str):
        self.system_instruction = system_instruction
        self.llm = llm
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
        # Let the LLM handle the conversation history directly
        # Don't build a context string with history - that's duplicating what the LLM already does
        return self.llm.generate(prompt=user_input, system_instruction=self.system_instruction)
    
    def _build_context_from_history(self) -> str:
        """Build a context string from the conversation history."""
        if not self._history:
            return ""
        
        context = []
        for entry in self._history:
            context.append(f"User: {entry['user_input']}")
            context.append(f"Assistant: {entry['response']}")
        
        return "\n".join(context)