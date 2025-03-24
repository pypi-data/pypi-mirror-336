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
        # Build context from conversation history
        context = self._build_context_from_history()
        
        # Append the current user input to the context
        if context:
            context += f"\nUser: {user_input}"
            prompt = f"Previous conversation:\n{context}\n\nRespond to the user's last message."
        else:
            prompt = user_input
        
        # Use the LLM to generate a response with the full context
        return self.llm.generate(prompt=prompt, system_instruction=self.system_instruction)
    
    def _build_context_from_history(self) -> str:
        """Build a context string from the conversation history."""
        if not self._history:
            return ""
        
        context = []
        for entry in self._history:
            context.append(f"User: {entry['user_input']}")
            context.append(f"Assistant: {entry['response']}")
        
        return "\n".join(context)