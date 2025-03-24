from typing import Optional, List, Dict, Any

class LLM:
    """A base class for language model interactions."""
    
    def __init__(self, 
                 model_name: str = "https://model.lmstudio.ai/download/lmstudio-community/Llama-3.3-70B-Instruct-GGUF",
                 host: str = "host.docker.internal:1234",
                 max_tokens: int = 100,
                 temperature: float = 0.7,
                 top_p: float = 1.0,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0,
                 stop_sequences: Optional[list[str]] = None):
        """Initialize the LLM.
        
        Args:
            model_name: The name/identifier of the language model to use
            host: The host URL where the model is served
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
            top_p: Nucleus sampling parameter (0-1) 
            frequency_penalty: Penalty for token frequency (-2 to 2)
            presence_penalty: Penalty for token presence (-2 to 2)
            stop_sequences: Optional list of sequences where generation should stop
        """
        self.model_name = model_name
        self.host = host
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop_sequences = stop_sequences or []
        
    def generate(self, 
                 prompt: Optional[str] = None, 
                 system_instruction: Optional[str] = None,
                 messages: Optional[List[Dict[str, str]]] = None,
                 tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        """Generate a response from the language model.
        
        Args:
            prompt: The user prompt/input text (for backwards compatibility)
            system_instruction: Optional system instruction to guide model behavior
            messages: List of message objects representing the conversation history
            tools: Optional list of tool schemas for function calling
            
        Returns:
            The generated response (format depends on implementation)
            
        Raises:
            NotImplementedError: This base class doesn't implement generation
        """
        raise NotImplementedError("Subclasses must implement generate()")

