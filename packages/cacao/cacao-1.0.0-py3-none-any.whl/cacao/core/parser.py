"""Core documentation parser for CacaoDocs."""
import re
import inspect
from typing import Dict, Any, Optional, List
from functools import wraps

from .config import Config
from ..utils.error_handler import ErrorHandler, ParserError
from ..plugins.plugin_manager import PluginManager
from ..plugins.base_plugin import ParserPlugin

class Parser:
    """Core documentation parser with plugin support."""

    _instance = None
    _default_parser = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Parser, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls) -> None:
        """Initialize the parser and load plugins."""
        # Load parser plugins
        parser_plugins = PluginManager.get_plugins_by_type(ParserPlugin)
        if parser_plugins:
            cls._default_parser = parser_plugins[0]
        else:
            cls._default_parser = None

    @classmethod
    @ErrorHandler.error_handler("ParserError")
    def parse_docstring(cls, docstring: str, doc_type: str = "docs") -> Dict[str, Any]:
        """
        Parse a docstring using available plugins.
        
        Args:
            docstring: The docstring to parse
            doc_type: Type of documentation ('api', 'types', 'docs')
            
        Returns:
            Dict containing parsed metadata and content
        """
        if not docstring:
            return {}

        # Get parser plugins
        parser_plugins = PluginManager.get_plugins_by_type(ParserPlugin)
        
        # Try each parser plugin
        errors = []
        for plugin in parser_plugins:
            try:
                result = plugin.parse_docstring(docstring, doc_type)
                if result:
                    return result
            except Exception as e:
                errors.append(f"{plugin.name}: {str(e)}")
                continue
        
        # If no plugins or all plugins failed, use default parsing
        if not parser_plugins or errors:
            return cls._default_parse(docstring, doc_type)
            
        return {}

    @classmethod
    def _default_parse(cls, docstring: str, doc_type: str) -> Dict[str, Any]:
        """Default parsing implementation when no plugins are available."""
        docstring = inspect.cleandoc(docstring)
        
        # Basic metadata patterns
        patterns = {
            "endpoint": r"Endpoint:\s*(.*)",
            "method": r"Method:\s*(.*)",
            "version": r"Version:\s*(.*)",
            "status": r"Status:\s*(.*)",
            "description": r"Description:\s*(.*?)(?=\n\s*(?:Args|Returns|Raises|$))",
            "args": r"Args:\s*(.*?)(?=\n\s*(?:Returns|Raises|$))",
            "returns": r"Returns:\s*(.*?)(?=\n\s*(?:Raises|$))",
            "raises": r"Raises:\s*(.*?)(?=\n\s*$)"
        }
        
        metadata = {}
        
        # Extract metadata using patterns
        for key, pattern in patterns.items():
            match = re.search(pattern, docstring, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if content:
                    metadata[key] = content
        
        # Parse arguments if present
        if "args" in metadata:
            args_dict = {}
            args_lines = metadata["args"].split("\n")
            for line in args_lines:
                line = line.strip()
                if line:
                    # Match pattern: arg_name (type): description
                    arg_match = re.match(r"(\w+)\s*\(([^)]+)\)\s*:\s*(.+)?", line)
                    if arg_match:
                        arg_name = arg_match.group(1)
                        arg_type = arg_match.group(2)
                        arg_desc = arg_match.group(3) or ""
                        args_dict[arg_name] = {
                            "type": arg_type,
                            "description": arg_desc
                        }
            metadata["args"] = args_dict
        
        return metadata

    @classmethod
    def extract_type_info(cls, obj: Any) -> Dict[str, Any]:
        """Extract type information from an object."""
        type_info = {
            "name": obj.__class__.__name__,
            "module": obj.__class__.__module__,
            "doc": inspect.getdoc(obj) or "",
            "attributes": {},
            "methods": {}
        }
        
        # Get attributes
        for name, value in inspect.getmembers(obj):
            if not name.startswith("_"):  # Skip private/protected
                if not callable(value):
                    type_info["attributes"][name] = {
                        "type": type(value).__name__,
                        "doc": inspect.getdoc(value) or ""
                    }
                else:
                    # Get method signature
                    try:
                        sig = inspect.signature(value)
                        type_info["methods"][name] = {
                            "signature": str(sig),
                            "doc": inspect.getdoc(value) or "",
                            "parameters": {
                                param_name: {
                                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else None,
                                    "default": str(param.default) if param.default != inspect.Parameter.empty else None
                                }
                                for param_name, param in sig.parameters.items()
                            }
                        }
                    except ValueError:
                        # Skip if can't get signature
                        continue
                        
        return type_info

    @classmethod
    def parse_module(cls, module) -> Dict[str, Any]:
        """Parse documentation from a Python module."""
        module_info = {
            "name": module.__name__,
            "doc": inspect.getdoc(module) or "",
            "classes": {},
            "functions": {},
            "variables": {}
        }
        
        for name, obj in inspect.getmembers(module):
            if not name.startswith("_"):  # Skip private/protected
                if inspect.isclass(obj):
                    module_info["classes"][name] = cls.extract_type_info(obj)
                elif inspect.isfunction(obj):
                    module_info["functions"][name] = {
                        "doc": inspect.getdoc(obj) or "",
                        "signature": str(inspect.signature(obj))
                    }
                elif not callable(obj):
                    module_info["variables"][name] = {
                        "type": type(obj).__name__,
                        "value": str(obj)
                    }
                    
        return module_info
