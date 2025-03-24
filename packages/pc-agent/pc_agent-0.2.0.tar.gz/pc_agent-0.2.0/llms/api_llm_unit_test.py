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