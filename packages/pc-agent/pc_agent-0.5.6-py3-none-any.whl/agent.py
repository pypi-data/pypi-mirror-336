from llms.llm import LLM
from tools.base_tool import BaseTool
from typing import Optional, List, Dict, Any
import json

class Agent:
    def __init__(self, system_instruction: str, llm: LLM, goal: str, tools: List[BaseTool] = []):
        self.system_instruction = system_instruction
        self.llm = llm
        self.goal = goal
        self._history = []  # Will store list of message dictionaries
        self._response = None
        
        # Store tools in a dictionary for easy lookup
        self.tools = {}
        for tool in tools:
            self.tools[tool.name] = tool

    def run(self, user_input: str):
        """
        Process user input, generate a response using the LLM, and handle any tool calls.
        
        Args:
            user_input: The user's input text
            
        Returns:
            The final response from the assistant
        """
        # Append user input as a message to history
        self._history.append({"role": "user", "content": user_input})
        
        while True:
            # Build messages from history
            messages = list(self._history)
            
            # Add system instruction if not already present
            if not any(msg.get("role") == "system" for msg in messages):
                messages.insert(0, {"role": "system", "content": self.system_instruction})
            
            # Collect tool schemas if we have tools
            tool_schemas = None
            if self.tools:
                tool_schemas = [tool.schema for tool in self.tools.values()]
            
            # Generate response from LLM with tool schemas
            response = self.llm.generate(messages=messages, tools=tool_schemas)
            
            # Check if the response contains tool calls
            message = response.get("choices", [{}])[0].get("message", {})
            self._history.append(message)
            
            if "tool_calls" in message:
                # Process each tool call
                for tool_call in message.get("tool_calls", []):
                    tool_call_id = tool_call.get("id")
                    function = tool_call.get("function", {})
                    tool_name = function.get("name")
                    
                    if tool_name in self.tools:
                        try:
                            # Parse arguments using json.loads for security
                            arguments = function.get("arguments", "{}")
                            args = {}
                            if arguments:
                                args = json.loads(arguments)
                            
                            # Execute the tool
                            tool = self.tools[tool_name]
                            result = tool.execute(**args)
                            
                            # Add the tool result to the history
                            self._history.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": str(result)
                            })
                        except Exception as e:
                            # Add error result to history
                            self._history.append({
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": f"Error: {str(e)}"
                            })
                # Continue the loop to get another response with tool results incorporated
                continue
            else:
                # No tool calls, we have our final response
                self._response = message.get("content", "")
                break
        
        return self._response

    def _get_response(self, user_input: str):
        """Legacy method maintained for compatibility."""
        return self.run(user_input)
    
    def _build_context_from_history(self) -> str:
        """Legacy method maintained for compatibility."""
        if not self._history:
            return ""
        
        context = []
        for entry in self._history:
            if entry.get("role") == "user":
                context.append(f"User: {entry['content']}")
            elif entry.get("role") == "assistant":
                context.append(f"Assistant: {entry['content']}")
        
        return "\n".join(context)