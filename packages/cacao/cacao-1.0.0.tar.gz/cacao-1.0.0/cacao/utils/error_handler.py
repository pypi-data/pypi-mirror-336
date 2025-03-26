"""Error handling system for CacaoDocs."""
import logging
from typing import Optional, Dict, Any, Type
from functools import wraps

class CacaoDocsError(Exception):
    """Base exception class for CacaoDocs."""
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)

class ConfigError(CacaoDocsError):
    """Configuration related errors."""
    pass

class PluginError(CacaoDocsError):
    """Plugin related errors."""
    pass

class ParserError(CacaoDocsError):
    """Parser related errors."""
    pass

class RenderError(CacaoDocsError):
    """Rendering related errors."""
    pass

class ErrorHandler:
    """Centralized error handling for CacaoDocs."""
    
    _logger = logging.getLogger("CacaoDocs")
    _error_registry: Dict[str, Type[CacaoDocsError]] = {
        "ConfigError": ConfigError,
        "PluginError": PluginError,
        "ParserError": ParserError,
        "RenderError": RenderError
    }

    @classmethod
    def setup_logging(cls, level: int = logging.INFO) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    @classmethod
    def handle_error(cls, error_type: str, message: str, details: Dict[str, Any] = None) -> None:
        """Handle an error by logging it and raising the appropriate exception."""
        error_class = cls._error_registry.get(error_type, CacaoDocsError)
        cls._logger.error(f"{error_type}: {message}", extra=details or {})
        raise error_class(message, error_type, details)

    @classmethod
    def error_handler(cls, error_type: str = None):
        """Decorator for handling errors in functions."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if isinstance(e, CacaoDocsError):
                        raise e
                    cls.handle_error(
                        error_type or "UnknownError",
                        str(e),
                        {"function": func.__name__, "args": args, "kwargs": kwargs}
                    )
            return wrapper
        return decorator

    @classmethod
    def register_error_type(cls, error_type: str, error_class: Type[CacaoDocsError]) -> None:
        """Register a new error type."""
        cls._error_registry[error_type] = error_class

    @classmethod
    def get_error_types(cls) -> Dict[str, Type[CacaoDocsError]]:
        """Get all registered error types."""
        return cls._error_registry.copy()

    @classmethod
    def format_error(cls, error: CacaoDocsError) -> Dict[str, Any]:
        """Format an error for API responses."""
        return {
            "error": {
                "type": error.error_code,
                "message": error.message,
                "details": error.details
            }
        }
