import pytest
import os
import time
from llms.api_llm import OpenAILLM
import requests
import json


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
            
    def test_conversation_history_persistence(self, api_key):
        """Test that conversation history is maintained across multiple calls."""
        # Arrange
        llm = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0  # Use deterministic responses for more stable tests
        )
        
        # Act - First turn: Ask about a specific topic
        first_prompt = "What is the capital of France?"
        first_response = llm.generate(first_prompt)
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        # Act - Second turn: Follow-up question referring to previous context
        second_prompt = "What is its population?"
        second_response = llm.generate(second_prompt)
        
        # Assert
        assert "Paris" in first_response
        assert len(second_response) > 0
        
        # The follow-up should mention Paris since the context should be preserved
        assert "Paris" in second_response or "paris" in second_response.lower()
        
        # Check that the conversation history contains all exchanges
        history = llm.get_conversation_history()
        assert len(history) == 4  # user + assistant + user + assistant
        assert history[0]["role"] == "user"
        assert history[0]["content"] == first_prompt
        assert history[1]["role"] == "assistant" 
        assert history[2]["role"] == "user"
        assert history[2]["content"] == second_prompt
        assert history[3]["role"] == "assistant"
        
    def test_reset_conversation_integration(self, api_key):
        """Test that resetting conversation clears the history and affects responses."""
        # Arrange
        llm = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0
        )
        
        # Act - Set up a conversation
        llm.generate("My name is John Doe.")
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        # Before reset: The model should remember the name
        pre_reset_response = llm.generate("What's my name?")
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        # Reset the conversation
        llm.reset_conversation()
        
        # After reset: The model should not remember the name
        post_reset_response = llm.generate("What's my name?")
        
        # Assert
        assert "John" in pre_reset_response or "john" in pre_reset_response.lower()
        assert "Doe" in pre_reset_response or "doe" in pre_reset_response.lower()
        
        # After reset, the model shouldn't know the name (response should be different)
        assert "John" not in post_reset_response and "john" not in post_reset_response.lower()
        assert "Doe" not in post_reset_response and "doe" not in post_reset_response.lower()
        
        # Conversation history should now only have the latest exchange
        history = llm.get_conversation_history()
        assert len(history) == 2  # just user + assistant from post-reset
        
    def test_add_message_to_history_integration(self, api_key):
        """Test that manually adding messages affects model responses."""
        # Arrange
        llm = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0
        )
        
        # Act - Manually build a conversation history
        llm.add_message_to_history("system", "You are a calculator.")
        llm.add_message_to_history("user", "One")
        llm.add_message_to_history("assistant", "next number")
        llm.add_message_to_history("user", "Two")
        
        # Generate a response based on the manually constructed history
        response = llm.generate("what is the result?")
        
        # Assert
        assert len(response) > 0
        
        # The response should be the sum of the last two numbers
        assert "3" in response.lower() or "three" in response.lower(), f"Expected '3' or 'three' in response but got: {response}"
        
        # History should contain all 4 messages (3 manual + 1 new)
        history = llm.get_conversation_history()
        assert len(history) == 6  # system + user + assistant + user + user + assistant
        
    def test_system_instruction_persistence(self, api_key):
        """Test that system instructions persist across conversation turns."""
        # Arrange
        llm = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=50,
            temperature=0.0
        )
        
        # Add a system instruction in the first call
        system_instruction = "You are a medieval knight who speaks in old English."
        first_response = llm.generate("Introduce yourself.", system_instruction)
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        # Second call without explicit system instruction
        second_response = llm.generate("What weapons do you use?")
        
        # Assert
        # Both responses should use old English style due to persisted system instruction
        medieval_terms = ["thy", "thou", "thee", "hast", "art", "doth", "hath", "ye", "verily", "forsooth"]
        
        first_medieval_count = sum(term in first_response.lower() for term in medieval_terms)
        second_medieval_count = sum(term in second_response.lower() for term in medieval_terms)
        
        # At least one of the responses should contain medieval language
        assert first_medieval_count > 0 or second_medieval_count > 0, \
            f"Responses don't contain medieval language: {first_response} / {second_response}"
            
        # The system message should be preserved in history
        history = llm.get_conversation_history()
        assert any(msg["role"] == "system" and msg["content"] == system_instruction for msg in history)

    def test_no_duplicate_conversation_in_api_request(self, api_key, mocker):
        """Test that API requests don't include duplicated conversation in the message content."""
        # Arrange 
        # Capture the request to inspect it
        original_post = requests.post
        
        # This will let us inspect what's actually sent to the API
        def mock_post(url, **kwargs):
            payload = json.loads(kwargs["data"])
            
            # Assert that no user message contains "Previous conversation" or duplicated content
            for msg in payload["messages"]:
                if msg["role"] == "user":
                    assert "Previous conversation" not in msg["content"]
                    
            # Let the real request go through for this integration test
            return original_post(url, **kwargs)
            
        mocker.patch("requests.post", side_effect=mock_post)
        
        llm = OpenAILLM(
            model_name="gpt-3.5-turbo",
            api_key=api_key,
            max_tokens=30,
            temperature=0.0
        )
        
        # Act - First message
        llm.generate("My name is Alex.")
        
        # Wait to avoid rate limits
        time.sleep(1)
        
        # Act - Follow-up question
        llm.generate("What's my name?")
        
        # No assertion needed here - the mock_post function does the validation 