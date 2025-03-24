import os
import requests
import json
from typing import Optional
from llms.llm import LLM


class OpenAILLM(LLM):
    """OpenAI implementation of the LLM interface."""
    
    def __init__(self, 
                 model_name: str = "gpt-4o",
                 host: str = "https://api.openai.com",
                 api_key: Optional[str] = None,
                 organization: Optional[str] = None,
                 max_tokens: int = 100,
                 temperature: float = 0.7,
                 top_p: float = 1.0,
                 frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0,
                 stop_sequences: Optional[list[str]] = None):
        """Initialize the OpenAI LLM.
        
        Args:
            model_name: The OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4")
            host: The host URL for the OpenAI API or compatible service
            api_key: OpenAI API key. If None, it will try to use OPENAI_API_KEY env var
            organization: OpenAI organization ID. If None, it will try to use OPENAI_ORG_ID env var
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0-1)
            top_p: Nucleus sampling parameter (0-1) 
            frequency_penalty: Penalty for token frequency (-2 to 2)
            presence_penalty: Penalty for token presence (-2 to 2)
            stop_sequences: Optional list of sequences where generation should stop
        """
        super().__init__(
            model_name=model_name,
            host=host,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop_sequences=stop_sequences
        )
        
        # Set API key from args or environment variable
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY environment variable")
        
        # Set organization if provided or from environment variable
        self.organization = organization or os.environ.get("OPENAI_ORG_ID")
        
        # Assume host already includes protocol
        self.api_url = f"{self.host}/v1/chat/completions"
        
        # Set up headers
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if self.organization:
            self.headers["OpenAI-Organization"] = self.organization
    
    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate a response using OpenAI's API.
        
        Args:
            prompt: The user prompt/input text
            system_instruction: Optional system instruction to guide model behavior
            
        Returns:
            The generated response text
        """
        messages = []
        
        # Add system message if provided
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        # Add user message
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request payload
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }
        
        # Add stop sequences if provided
        if self.stop_sequences:
            payload["stop"] = self.stop_sequences
        
        # Make the API request
        response = requests.post(
            self.api_url,
            headers=self.headers,
            data=json.dumps(payload)
        )
        
        # Check for errors
        response.raise_for_status()
        
        # Parse the response JSON
        response_data = response.json()
        
        # Extract and return the generated text
        return response_data["choices"][0]["message"]["content"].strip()
