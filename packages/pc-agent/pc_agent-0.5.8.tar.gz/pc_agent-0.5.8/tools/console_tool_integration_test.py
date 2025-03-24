import pytest
import os
import tempfile
import platform
from pathlib import Path

from tools.console_tool import ConsoleTool


class TestConsoleToolIntegration:
    """Integration test suite for the ConsoleTool class with real console commands."""
    
    @pytest.fixture
    def console_tool(self) -> ConsoleTool:
        """Fixture that returns a ConsoleTool instance."""
        return ConsoleTool()
    
    @pytest.fixture
    def temp_dir(self):
        """Fixture that creates a temporary directory and cleans it up after the test."""
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield tmpdirname
    
    def test_execute_echo_command(self, console_tool: ConsoleTool):
        """Test executing a real echo command."""
        # Arrange
        test_string = "Hello from integration test"
        
        # Act
        result = console_tool.execute(command=f"echo {test_string}")
        
        # Assert
        assert result["returncode"] == 0
        assert test_string in result["stdout"]
        assert not result["stderr"]
    
    def test_execute_directory_listing(self, console_tool: ConsoleTool):
        """Test executing a real directory listing command."""
        # Act
        result = console_tool.execute(command="ls -la" if platform.system() != "Windows" else "dir")
        
        # Assert
        assert result["returncode"] == 0
        assert result["stdout"]  # Should not be empty
    
    def test_execute_command_with_error(self, console_tool: ConsoleTool):
        """Test executing a command that should return an error."""
        # Act
        result = console_tool.execute(command="ls /nonexistent_directory")
        
        # Assert
        assert result["returncode"] != 0
        assert "No such file or directory" in result["stderr"] or "Cannot find the path specified" in result["stderr"]
    
    def test_execute_command_with_pipe(self, console_tool: ConsoleTool):
        """Test executing a command with a pipe."""
        # Arrange
        search_string = "test"
        
        # Act
        result = console_tool.execute(command=f"echo 'This is a test string' | grep {search_string}")
        
        # Assert
        assert result["returncode"] == 0
        assert search_string in result["stdout"]
    
    def test_execute_command_with_env_vars(self, console_tool: ConsoleTool):
        """Test executing a command that uses environment variables."""
        # Act
        if platform.system() != "Windows":
            result = console_tool.execute(command="TEST_VAR='integration test' && echo $TEST_VAR")
        else:
            result = console_tool.execute(command="set TEST_VAR=integration test && echo %TEST_VAR%")
        
        # Assert
        assert result["returncode"] == 0
        assert "integration test" in result["stdout"]
    
    def test_file_creation_and_reading(self, console_tool: ConsoleTool, temp_dir: str):
        """Test creating a file and reading its contents."""
        # Arrange
        test_content = "Integration test content"
        test_file = Path(temp_dir) / "test_file.txt"
        
        # Act - Create file
        result1 = console_tool.execute(command=f"echo '{test_content}' > {test_file}")
        
        # Act - Read file
        result2 = console_tool.execute(command=f"cat {test_file}" if platform.system() != "Windows" else f"type {test_file}")
        
        # Assert
        assert result1["returncode"] == 0
        assert result2["returncode"] == 0
        assert test_content in result2["stdout"]
    
    def test_command_timeout(self, console_tool: ConsoleTool):
        """Test command timeout functionality."""
        # Act
        result = console_tool.execute(command="sleep 3" if platform.system() != "Windows" else "timeout 3", timeout=1)
        
        # Assert
        assert "error" in result
        assert result["error"] == "Command execution timed out"
        assert result["timeout"] == 1 