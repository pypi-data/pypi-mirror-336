"""
Base Tool for LLM integration.
This module provides a foundation class for building tools that can be used with Language Models.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """
    Abstract base class for all LLM tools.
    
    All tools should inherit from this class and implement the required methods.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize a BaseTool.
        
        Args:
            name: The name of the tool, used for tool selection by the LLM
            description: A detailed description of what the tool does and how to use it
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool's functionality.
        
        All derived tools must implement this method to define their specific behavior.
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            Dict containing the results of the tool execution
        """
        pass
    
    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        """
        Get the schema for this tool in OpenAI function calling format.
        
        All derived tools must implement this method to define their schema.
        
        Returns:
            Dict containing the tool schema in OpenAI function calling format
        """
        pass
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert the tool to a dictionary representation (for API communication).
        
        Returns:
            Dictionary with tool name and description
        """
        return {
            "name": self.name,
            "description": self.description
        }
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the tool.
        Can be overridden by subclasses to provide additional metadata.
        
        Returns:
            Dictionary with tool metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__
        }
    
    def validate_args(self, **kwargs) -> bool:
        """
        Validate the arguments passed to the tool.
        Can be overridden by subclasses to provide argument validation.
        
        Args:
            **kwargs: Arguments to validate
            
        Returns:
            True if arguments are valid, False otherwise
        """
        return True
    
    def __str__(self) -> str:
        """String representation of the tool."""
        return f"{self.name}: {self.description}"
