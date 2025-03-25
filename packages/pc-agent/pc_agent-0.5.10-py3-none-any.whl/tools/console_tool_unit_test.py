import pytest
from pytest_mock import MockerFixture
from typing import Dict, Any
import subprocess

from tools.console_tool import ConsoleTool


class TestConsoleTool:
    """Test suite for the ConsoleTool class."""
    
    @pytest.fixture
    def console_tool(self) -> ConsoleTool:
        """Fixture that returns a ConsoleTool instance."""
        return ConsoleTool()
    
    def test_initialization(self, console_tool: ConsoleTool):
        """Test that ConsoleTool is initialized with correct attributes."""
        # Assert
        assert console_tool.name == "console"
        assert console_tool.description == "Execute arbitrary commands in the system shell without restrictions."
    
    def test_to_dict(self, console_tool: ConsoleTool):
        """Test the to_dict method returns the correct dictionary."""
        # Arrange
        expected_dict = {
            "name": "console",
            "description": "Execute arbitrary commands in the system shell without restrictions."
        }
        
        # Act
        result = console_tool.to_dict()
        
        # Assert
        assert result == expected_dict
    
    def test_metadata(self, console_tool: ConsoleTool):
        """Test the metadata property returns the correct dictionary."""
        # Arrange
        expected_metadata = {
            "name": "console",
            "description": "Execute arbitrary commands in the system shell without restrictions.",
            "type": "ConsoleTool"
        }
        
        # Act
        result = console_tool.metadata
        
        # Assert
        assert result == expected_metadata
    
    def test_schema(self, console_tool: ConsoleTool):
        """Test the schema property returns the correct OpenAI function format."""
        # Act
        schema = console_tool.schema
        
        # Assert
        assert schema["type"] == "function"
        assert schema["function"]["name"] == "console"
        assert schema["function"]["description"] == "Execute arbitrary commands in the system shell without restrictions."
        
        # Check parameters
        parameters = schema["function"]["parameters"]
        assert parameters["type"] == "object"
        
        # Check properties
        properties = parameters["properties"]
        assert "command" in properties
        assert properties["command"]["type"] == "string"
        assert "timeout" in properties
        assert properties["timeout"]["type"] == "integer"
        
        # Check required fields
        assert "required" in parameters
        assert "command" in parameters["required"]
    
    def test_validate_args_with_command(self, console_tool: ConsoleTool):
        """Test that validate_args returns True when command is provided."""
        # Act
        result = console_tool.validate_args(command="echo hello")
        
        # Assert
        assert result is True
    
    def test_validate_args_without_command(self, console_tool: ConsoleTool):
        """Test that validate_args returns False when command is not provided."""
        # Act
        result = console_tool.validate_args(other_arg="value")
        
        # Assert
        assert result is False
    
    def test_execute_command_success(self, console_tool: ConsoleTool, mocker: MockerFixture):
        """Test executing a command successfully."""
        # Arrange
        mock_process = mocker.MagicMock()
        mock_process.stdout = "command output"
        mock_process.stderr = ""
        mock_process.returncode = 0
        
        mocker.patch("subprocess.run", return_value=mock_process)
        
        # Act
        result = console_tool.execute(command="echo hello")
        
        # Assert
        assert result["stdout"] == "command output"
        assert result["stderr"] == ""
        assert result["returncode"] == 0
        subprocess.run.assert_called_once_with(
            "echo hello",
            shell=True,
            capture_output=True,
            text=True,
            timeout=None
        )
    
    def test_execute_command_with_timeout(self, console_tool: ConsoleTool, mocker: MockerFixture):
        """Test executing a command with timeout."""
        # Arrange
        mock_process = mocker.MagicMock()
        mock_process.stdout = "command output"
        mock_process.stderr = ""
        mock_process.returncode = 0
        
        mocker.patch("subprocess.run", return_value=mock_process)
        
        # Act
        result = console_tool.execute(command="sleep 1", timeout=5)
        
        # Assert
        subprocess.run.assert_called_once_with(
            "sleep 1",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
    
    def test_execute_command_timeout_expired(self, console_tool: ConsoleTool, mocker: MockerFixture):
        """Test handling of command timeout expiration."""
        # Arrange
        mocker.patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="sleep 10", timeout=1))
        
        # Act
        result = console_tool.execute(command="sleep 10", timeout=1)
        
        # Assert
        assert "error" in result
        assert result["error"] == "Command execution timed out"
        assert result["command"] == "sleep 10"
        assert result["timeout"] == 1
    
    def test_execute_command_exception(self, console_tool: ConsoleTool, mocker: MockerFixture):
        """Test handling of general exceptions during command execution."""
        # Arrange
        mocker.patch("subprocess.run", side_effect=Exception("Test error"))
        
        # Act
        result = console_tool.execute(command="invalid command")
        
        # Assert
        assert "error" in result
        assert result["error"] == "Test error"
        assert result["command"] == "invalid command" 