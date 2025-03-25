"""
Console Tool for executing commands in the system shell.
This module provides a tool for running console commands without restrictions.
"""
import subprocess
from typing import Dict, Any, Optional
from .base_tool import BaseTool


class ConsoleTool(BaseTool):
    """
    Tool for executing arbitrary commands in the system shell.
    
    This tool allows running console commands without restrictions.
    """
    
    def __init__(self):
        """
        Initialize the ConsoleTool.
        """
        super().__init__(
            name="console",
            description="Execute arbitrary commands in the system shell without restrictions."
        )
    
    def execute(self, command: str, timeout: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """
        Execute a command in the system shell.
        
        Args:
            command: The command to execute
            timeout: Optional timeout in seconds
            **kwargs: Additional arguments
            
        Returns:
            Dict containing the results of the command execution:
                - stdout: Standard output as string
                - stderr: Standard error as string
                - returncode: Process return code
        """
        try:
            # Run the command in the shell
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "returncode": process.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "error": "Command execution timed out",
                "command": command,
                "timeout": timeout
            }
        except Exception as e:
            return {
                "error": str(e),
                "command": command
            }
    
    @property
    def schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool in OpenAI function calling format.
        
        Returns:
            Dict containing the tool schema
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The command to execute in the system shell"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Optional timeout in seconds for command execution"
                        }
                    },
                    "required": ["command"]
                }
            }
        }
    
    def validate_args(self, **kwargs) -> bool:
        """
        Validate the arguments passed to the tool.
        
        Args:
            command: The command to execute must be provided
            
        Returns:
            True if arguments are valid, False otherwise
        """
        return "command" in kwargs 