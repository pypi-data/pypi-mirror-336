import pytest
from pytest_mock import MockerFixture
from typing import Dict, Any

from tools.base_tool import BaseTool


# Concrete implementation of BaseTool for testing
class MockTool(BaseTool):
    def execute(self, **kwargs) -> Dict[str, Any]:
        return {"result": "mock_result", "args": kwargs}
    
    @property
    def schema(self) -> Dict[str, Any]:
        """
        Implement the required schema property for testing.
        
        Returns:
            Dict with a simple schema definition for the mock tool
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "arg1": {
                            "type": "string",
                            "description": "Mock argument 1"
                        },
                        "arg2": {
                            "type": "string",
                            "description": "Mock argument 2"
                        }
                    },
                    "required": ["arg1"]
                }
            }
        }


class TestBaseTool:
    """Test suite for the BaseTool class."""
    
    @pytest.fixture
    def mock_tool(self) -> MockTool:
        """Fixture that returns a concrete implementation of BaseTool."""
        return MockTool(name="mock_tool", description="A mock tool for testing")
    
    def test_initialization(self, mock_tool: MockTool):
        """Test that BaseTool is initialized with correct attributes."""
        # Arrange
        expected_name = "mock_tool"
        expected_description = "A mock tool for testing"
        
        # Assert
        assert mock_tool.name == expected_name
        assert mock_tool.description == expected_description
    
    def test_to_dict(self, mock_tool: MockTool):
        """Test the to_dict method returns the correct dictionary."""
        # Arrange
        expected_dict = {
            "name": "mock_tool",
            "description": "A mock tool for testing"
        }
        
        # Act
        result = mock_tool.to_dict()
        
        # Assert
        assert result == expected_dict
    
    def test_metadata(self, mock_tool: MockTool):
        """Test the metadata property returns the correct dictionary."""
        # Arrange
        expected_metadata = {
            "name": "mock_tool",
            "description": "A mock tool for testing",
            "type": "MockTool"
        }
        
        # Act
        result = mock_tool.metadata
        
        # Assert
        assert result == expected_metadata
    
    def test_validate_args_default(self, mock_tool: MockTool):
        """Test that validate_args returns True by default."""
        # Act
        result = mock_tool.validate_args(arg1="value1", arg2="value2")
        
        # Assert
        assert result is True
    
    def test_str_representation(self, mock_tool: MockTool):
        """Test the string representation of the tool."""
        # Arrange
        expected_str = "mock_tool: A mock tool for testing"
        
        # Act
        result = str(mock_tool)
        
        # Assert
        assert result == expected_str
    
    def test_execute_implementation(self, mock_tool: MockTool):
        """Test that the concrete implementation of execute works correctly."""
        # Arrange
        test_args = {"arg1": "value1", "arg2": "value2"}
        expected_result = {"result": "mock_result", "args": test_args}
        
        # Act
        result = mock_tool.execute(**test_args)
        
        # Assert
        assert result == expected_result
    
    def test_abstract_method_requirement(self):
        """Test that BaseTool cannot be instantiated without implementing execute."""
        # Act & Assert
        with pytest.raises(TypeError):
            BaseTool(name="abstract_tool", description="This should fail")
    
    def test_schema_implementation(self, mock_tool: MockTool):
        """Test that the schema property returns the correct schema format."""
        # Act
        schema = mock_tool.schema
        
        # Assert
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "mock_tool"
        assert schema["function"]["description"] == "A mock tool for testing"
        
        # Check parameters
        parameters = schema["function"]["parameters"]
        assert parameters["type"] == "object"
        
        # Check properties
        properties = parameters["properties"]
        assert "arg1" in properties
        assert properties["arg1"]["type"] == "string"
        assert "arg2" in properties
        assert properties["arg2"]["type"] == "string"
        
        # Check required fields
        assert "required" in parameters
        assert "arg1" in parameters["required"] 