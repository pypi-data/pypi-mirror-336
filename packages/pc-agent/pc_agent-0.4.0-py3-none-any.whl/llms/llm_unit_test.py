import pytest
from llms.llm import LLM

class TestLLM:
    @pytest.fixture
    def llm(self):
        """Fixture that returns a default LLM instance"""
        return LLM()

    def test_default_initialization(self, llm):
        """Test that LLM initializes with default parameters"""
        # Arrange
        expected_model = "https://model.lmstudio.ai/download/lmstudio-community/Llama-3.3-70B-Instruct-GGUF"
        expected_host = "host.docker.internal:1234"
        
        # Act - LLM instance created by fixture
        
        # Assert
        assert llm.model_name == expected_model
        assert llm.host == expected_host
        assert llm.max_tokens == 100
        assert llm.temperature == 0.7
        assert llm.top_p == 1.0
        assert llm.frequency_penalty == 0.0
        assert llm.presence_penalty == 0.0
        assert llm.stop_sequences == []

    def test_custom_initialization(self):
        """Test that LLM initializes with custom parameters"""
        # Arrange
        expected_model = "custom-model"
        expected_host = "custom-host:5678"
        expected_tokens = 200
        expected_temp = 0.5
        expected_top_p = 0.9
        expected_freq_penalty = 0.1
        expected_pres_penalty = 0.2
        expected_stop = ["STOP", "END"]
        
        # Act
        llm = LLM(
            model_name=expected_model,
            host=expected_host, 
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
        assert llm.max_tokens == expected_tokens
        assert llm.temperature == expected_temp
        assert llm.top_p == expected_top_p
        assert llm.frequency_penalty == expected_freq_penalty
        assert llm.presence_penalty == expected_pres_penalty
        assert llm.stop_sequences == expected_stop

    def test_generate_not_implemented(self, llm):
        """Test that generate() raises NotImplementedError"""
        # Arrange
        test_prompt = "test prompt"
        
        # Act & Assert
        with pytest.raises(NotImplementedError):
            llm.generate(test_prompt)
