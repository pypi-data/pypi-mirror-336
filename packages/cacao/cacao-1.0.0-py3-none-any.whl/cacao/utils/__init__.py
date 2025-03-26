"""Utility functions and classes for CacaoDocs."""

from .error_handler import (
    ErrorHandler,
    CacaoDocsError,
    ConfigError,
    PluginError,
    ParserError,
    RenderError
)

__all__ = [
    "ErrorHandler",
    "CacaoDocsError",
    "ConfigError",
    "PluginError",
    "ParserError",
    "RenderError"
]
