import pytest
import json
import os
import requests
from llms.api_llm import OpenAILLM


class TestOpenAILLM:
    """Test suite for the OpenAILLM class."""
    
    @pytest.fixture
    def api_key(self):
        """Fixture that returns a mock API key."""
        return "test-api-key"
    
    @pytest.fixture
    def mock_response(self, mocker):
        """Fixture that returns a mock response object."""
        # Create a mock response with testing data
        mock = mocker.MagicMock()
        mock.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response."
                    }
                }
            ]
        }
        return mock
    
    def test_default_initialization(self, api_key):
        """Test that OpenAILLM initializes with default parameters."""
        # Arrange
        os.environ["OPENAI_API_KEY"] = api_key
        expected_model = "gpt-4o"
        expected_host = "https://api.openai.com"
        
        # Act
        llm = OpenAILLM()
        
        # Assert
        assert llm.model_name == expected_model
        assert llm.host == expected_host
        assert llm.api_key == api_key
        assert llm.max_tokens == 100
        assert llm.temperature == 0.7
        assert llm.top_p == 1.0
        assert llm.frequency_penalty == 0.0
        assert llm.presence_penalty == 0.0
        assert llm.stop_sequences == []
        assert llm.api_url == f"{expected_host}/v1/chat/completions"
        assert llm.message_history == []
    
    def test_custom_initialization(self, api_key):
        """Test that OpenAILLM initializes with custom parameters."""
        # Arrange
        expected_model = "gpt-3.5-turbo"
        expected_host = "https://api.openai.com"
        expected_org = "test-org"
        expected_tokens = 200
        expected_temp = 0.5
        expected_top_p = 0.9
        expected_freq_penalty = 0.1
        expected_pres_penalty = 0.2
        expected_stop = ["STOP", "END"]
        
        # Act
        llm = OpenAILLM(
            model_name=expected_model,
            host=expected_host,
            api_key=api_key,
            organization=expected_org,
            max_tokens=expected_tokens,
            temperature=expected_temp,
            top_p=expected_top_p,
            frequency_penalty=expected_freq_penalty,
            presence_penalty=expected_pres_penalty,
            stop_sequences=expected_stop
        )
        
        # Assert
        assert llm.model_name == expected_model
        assert llm.host == expected_host
        assert llm.api_key == api_key
        assert llm.organization == expected_org
        assert llm.max_tokens == expected_tokens
        assert llm.temperature == expected_temp
        assert llm.top_p == expected_top_p
        assert llm.frequency_penalty == expected_freq_penalty
        assert llm.presence_penalty == expected_pres_penalty
        assert llm.stop_sequences == expected_stop
        assert llm.api_url == f"{expected_host}/v1/chat/completions"
        assert "OpenAI-Organization" in llm.headers
        assert llm.headers["OpenAI-Organization"] == expected_org
        assert llm.message_history == []
    
    def test_missing_api_key(self, mocker):
        """Test that OpenAILLM raises an error when no API key is provided."""
        # Arrange - ensure environment variable is not set
        mocker.patch.dict(os.environ, {}, clear=True)
            
        # Act & Assert
        with pytest.raises(ValueError, match="OpenAI API key must be provided"):
            OpenAILLM()
    
    def test_generate_with_system_instruction(self, mocker, api_key, mock_response):
        """Test generate method with system instruction."""
        # Arrange
        requests_post = mocker.patch("requests.post", return_value=mock_response)
        test_prompt = "Hello, world!"
        test_system = "You are a helpful assistant."
        expected_response = "This is a test response."
        
        llm = OpenAILLM(api_key=api_key)
        
        # Act
        response = llm.generate(test_prompt, test_system)
        
        # Assert
        assert response == expected_response
        
        # Check that requests.post was called with the right arguments
        requests_post.assert_called_once()
        args, kwargs = requests_post.call_args
        
        # Check URL
        assert args[0] == f"{llm.host}/v1/chat/completions"
        
        # Check headers
        assert kwargs["headers"] == llm.headers
        
        # Check payload
        payload = json.loads(kwargs["data"])
        assert payload["model"] == llm.model_name
        assert payload["max_tokens"] == llm.max_tokens
        assert len(payload["messages"]) == 2
        assert payload["messages"][0]["role"] == "system"
        assert payload["messages"][0]["content"] == test_system
        assert payload["messages"][1]["role"] == "user"
        assert payload["messages"][1]["content"] == test_prompt
        
        # Check that message history was updated
        assert len(llm.message_history) == 3  # system + user + assistant
        assert llm.message_history[0]["role"] == "system"
        assert llm.message_history[0]["content"] == test_system
        assert llm.message_history[1]["role"] == "user"
        assert llm.message_history[1]["content"] == test_prompt
        assert llm.message_history[2]["role"] == "assistant"
        assert llm.message_history[2]["content"] == expected_response
    
    def test_generate_without_system_instruction(self, mocker, api_key, mock_response):
        """Test generate method without system instruction."""
        # Arrange
        requests_post = mocker.patch("requests.post", return_value=mock_response)
        test_prompt = "Hello, world!"
        expected_response = "This is a test response."
        
        llm = OpenAILLM(api_key=api_key)
        
        # Act
        response = llm.generate(test_prompt)
        
        # Assert
        assert response == expected_response
        
        # Check that requests.post was called with the right arguments
        requests_post.assert_called_once()
        args, kwargs = requests_post.call_args
        
        # Check payload
        payload = json.loads(kwargs["data"])
        assert len(payload["messages"]) == 1
        assert payload["messages"][0]["role"] == "user"
        assert payload["messages"][0]["content"] == test_prompt
        
        # Check that message history was updated
        assert len(llm.message_history) == 2  # user + assistant
        assert llm.message_history[0]["role"] == "user"
        assert llm.message_history[0]["content"] == test_prompt
        assert llm.message_history[1]["role"] == "assistant"
        assert llm.message_history[1]["content"] == expected_response
    
    def test_generate_with_stop_sequences(self, mocker, api_key, mock_response):
        """Test generate method with stop sequences."""
        # Arrange
        requests_post = mocker.patch("requests.post", return_value=mock_response)
        test_prompt = "Hello, world!"
        stop_sequences = ["STOP", "END"]
        
        llm = OpenAILLM(api_key=api_key, stop_sequences=stop_sequences)
        
        # Act
        llm.generate(test_prompt)
        
        # Assert - Check that stop sequences are in the payload
        args, kwargs = requests_post.call_args
        payload = json.loads(kwargs["data"])
        assert payload["stop"] == stop_sequences
    
    def test_api_error_handling(self, mocker, api_key):
        """Test that generate method handles API errors by raising them."""
        # Arrange
        error_response = mocker.MagicMock()
        error_response.raise_for_status.side_effect = Exception("API Error")
        mocker.patch("requests.post", return_value=error_response)
        
        llm = OpenAILLM(api_key=api_key)
        
        # Act & Assert
        with pytest.raises(Exception, match="API Error"):
            llm.generate("Test prompt")
            
    def test_reset_conversation(self, api_key):
        """Test that reset_conversation clears the message history."""
        # Arrange
        llm = OpenAILLM(api_key=api_key)
        llm.message_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        # Act
        llm.reset_conversation()
        
        # Assert
        assert llm.message_history == []
        
    def test_get_conversation_history(self, api_key):
        """Test that get_conversation_history returns the message history."""
        # Arrange
        llm = OpenAILLM(api_key=api_key)
        expected_history = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        llm.message_history = expected_history.copy()
        
        # Act
        actual_history = llm.get_conversation_history()
        
        # Assert
        assert actual_history == expected_history
        
    def test_add_message_to_history(self, api_key):
        """Test that add_message_to_history adds a message to the history."""
        # Arrange
        llm = OpenAILLM(api_key=api_key)
        
        # Act
        llm.add_message_to_history("system", "You are a helpful assistant.")
        llm.add_message_to_history("user", "Hello!")
        llm.add_message_to_history("assistant", "Hi there!")
        
        # Assert
        assert len(llm.message_history) == 3
        assert llm.message_history[0]["role"] == "system"
        assert llm.message_history[0]["content"] == "You are a helpful assistant."
        assert llm.message_history[1]["role"] == "user"
        assert llm.message_history[1]["content"] == "Hello!"
        assert llm.message_history[2]["role"] == "assistant"
        assert llm.message_history[2]["content"] == "Hi there!"
        
    def test_add_message_to_history_invalid_role(self, api_key):
        """Test that add_message_to_history raises an error for invalid roles."""
        # Arrange
        llm = OpenAILLM(api_key=api_key)
        
        # Act & Assert
        with pytest.raises(ValueError, match="Role must be one of"):
            llm.add_message_to_history("invalid-role", "This should fail.")
            
    def test_conversation_continuity(self, mocker, api_key):
        """Test that conversation history is maintained across multiple generate calls."""
        # Arrange
        mock_response1 = mocker.MagicMock()
        mock_response1.json.return_value = {
            "choices": [{"message": {"content": "First response."}}]
        }
        
        mock_response2 = mocker.MagicMock()
        mock_response2.json.return_value = {
            "choices": [{"message": {"content": "Second response."}}]
        }
        
        # Setup requests.post to return different responses on consecutive calls
        requests_post = mocker.patch("requests.post", side_effect=[mock_response1, mock_response2])
        
        llm = OpenAILLM(api_key=api_key)
        
        # Act - First conversation turn
        first_response = llm.generate("First question", "You are a helpful assistant.")
        
        # Act - Second conversation turn
        second_response = llm.generate("Second question")
        
        # Assert
        assert first_response == "First response."
        assert second_response == "Second response."
        
        # Check that the first call used only the initial messages
        call_args_list = requests_post.call_args_list
        assert len(call_args_list) == 2
        
        first_call_payload = json.loads(call_args_list[0][1]["data"])
        assert len(first_call_payload["messages"]) == 2
        assert first_call_payload["messages"][0]["role"] == "system"
        assert first_call_payload["messages"][1]["role"] == "user"
        assert first_call_payload["messages"][1]["content"] == "First question"
        
        # Check that the second call included the previous conversation
        second_call_payload = json.loads(call_args_list[1][1]["data"])
        assert len(second_call_payload["messages"]) == 4
        assert second_call_payload["messages"][0]["role"] == "system"
        assert second_call_payload["messages"][1]["role"] == "user"
        assert second_call_payload["messages"][1]["content"] == "First question"
        assert second_call_payload["messages"][2]["role"] == "assistant"
        assert second_call_payload["messages"][2]["content"] == "First response."
        assert second_call_payload["messages"][3]["role"] == "user"
        assert second_call_payload["messages"][3]["content"] == "Second question"
    
    def test_no_message_duplication_in_api_call(self, mocker, api_key):
        """Test that messages aren't duplicated in the API payload."""
        # Arrange
        mock_response1 = mocker.MagicMock()
        mock_response1.json.return_value = {
            "choices": [{"message": {"content": "Hello, I'm an assistant."}}]
        }
        
        mock_response2 = mocker.MagicMock()
        mock_response2.json.return_value = {
            "choices": [{"message": {"content": "Your name is Alex."}}]
        }
        
        # Setup requests.post to return different responses on consecutive calls
        requests_post = mocker.patch("requests.post", side_effect=[mock_response1, mock_response2])
        
        llm = OpenAILLM(api_key=api_key)
        
        # Act - First turn
        first_prompt = "My name is Alex."
        llm.generate(first_prompt)
        
        # Act - Second turn
        second_prompt = "What's my name?"
        llm.generate(second_prompt)
        
        # Assert - Check that the second call doesn't have the first conversation embedded in the prompt
        call_args_list = requests_post.call_args_list
        assert len(call_args_list) == 2
        
        # Check first API call
        first_call_payload = json.loads(call_args_list[0][1]["data"])
        assert len(first_call_payload["messages"]) == 1
        assert first_call_payload["messages"][0]["role"] == "user"
        assert first_call_payload["messages"][0]["content"] == "My name is Alex."
        
        # Check second API call
        second_call_payload = json.loads(call_args_list[1][1]["data"])
        assert len(second_call_payload["messages"]) == 3
        
        # Important: Check that the last user message doesn't contain the previous conversation
        assert second_call_payload["messages"][2]["role"] == "user"
        assert second_call_payload["messages"][2]["content"] == "What's my name?"
        assert "My name is Alex" not in second_call_payload["messages"][2]["content"]
        assert "Previous conversation" not in second_call_payload["messages"][2]["content"] 