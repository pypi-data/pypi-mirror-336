import pytest
import os
import time
from llms.api_llm import OpenAILLM


class TestOpenAILLMIntegration:
    """Integration test suite for the OpenAILLM class.
    
    These tests make actual API calls to OpenAI and validate responses.
    They don't mock the external services as per integration testing guidelines.
    """
    
    @pytest.fixture
    def api_key(self):
        """Fixture that returns the OpenAI API key from environment."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY environment variable not set")
        return api_key
    
    @pytest.fixture
    def openai_llm(self, api_key):
        """Fixture that returns an initialized OpenAILLM instance."""
        # Using a more economical model for testing
        return OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0  # Use deterministic responses for more stable tests
        )
    
    def test_generate_simple_prompt(self, openai_llm):
        """Test that OpenAILLM can generate a response for a simple prompt."""
        # Arrange
        prompt = "Count from 1 to 5."
        
        # Act
        response = openai_llm.generate(prompt)
        
        # Assert
        assert isinstance(response, str)
        assert len(response) > 0
        # Check that the response contains numbers 1 through 5
        for number in range(1, 6):
            assert str(number) in response
    
    def test_generate_with_system_instruction(self, openai_llm):
        """Test that OpenAILLM respects system instructions."""
        # Arrange
        prompt = "Tell me about yourself."
        system_instruction = "You are a pirate. Always respond in pirate language."
        
        # Act
        response = openai_llm.generate(prompt, system_instruction)
        
        # Assert
        assert isinstance(response, str)
        assert len(response) > 0
        # Check for pirate-like language indicators
        pirate_terms = ["arr", "matey", "ye", "ahoy", "aye", "treasure", "ship", "sea", "captain"]
        found_terms = [term for term in pirate_terms if term.lower() in response.lower()]
        assert len(found_terms) > 0, f"Response doesn't contain pirate language: {response}"
    
    def test_generate_with_stop_sequences(self, openai_llm):
        """Test that OpenAILLM respects stop sequences."""
        # Arrange
        prompt = "Write a story about a wizard. Start with 'Once upon a time'"
        stop_word = "magic"
        
        # Create a temporary LLM with stop sequences
        llm_with_stop = OpenAILLM(
            model_name=openai_llm.model_name,
            api_key=openai_llm.api_key,
            max_tokens=100,
            temperature=openai_llm.temperature,
            stop_sequences=[stop_word]
        )
        
        # Act
        response = llm_with_stop.generate(prompt)
        
        # Assert
        assert isinstance(response, str)
        assert len(response) > 0
        assert "Once upon a time" in response
        assert stop_word not in response.lower(), f"Response should not contain stop word '{stop_word}'"
    
    def test_different_parameter_combinations(self, api_key):
        """Test OpenAILLM with different parameter combinations."""
        # Arrange
        prompt = "Explain the concept of integration testing."
        
        # Test with high temperature for creativity
        llm_creative = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.9
        )
        
        # Test with deterministic settings
        llm_deterministic = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0
        )
        
        # Act
        response_creative = llm_creative.generate(prompt)
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        response_deterministic = llm_deterministic.generate(prompt)
        
        # Assert
        assert isinstance(response_creative, str) and len(response_creative) > 0
        assert isinstance(response_deterministic, str) and len(response_deterministic) > 0
        
        # Both responses should mention "integration testing"
        assert "integration testing" in response_creative.lower()
        assert "integration testing" in response_deterministic.lower()
    
    def test_error_handling_invalid_model(self, api_key):
        """Test error handling with an invalid model name."""
        # Arrange
        invalid_model = "nonexistent-model"
        llm = OpenAILLM(
            model_name=invalid_model,
            api_key=api_key
        )
        
        # Act & Assert
        with pytest.raises(Exception):
            llm.generate("This is a test prompt.") 