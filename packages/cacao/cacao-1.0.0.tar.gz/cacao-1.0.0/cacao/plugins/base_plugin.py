"""Base plugin interface for CacaoDocs."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BasePlugin(ABC):
    """Abstract base class for CacaoDocs plugins."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the plugin with optional configuration."""
        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the plugin. Called when the plugin is loaded."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources. Called when the plugin is unloaded."""
        pass

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

class ParserPlugin(BasePlugin):
    """Base class for parser plugins."""

    @abstractmethod
    def parse_docstring(self, docstring: str, doc_type: str) -> Dict[str, Any]:
        """Parse a docstring into structured data."""
        pass

class RendererPlugin(BasePlugin):
    """Base class for renderer plugins."""

    @abstractmethod
    def render(self, data: Dict[str, Any], template: str) -> str:
        """Render documentation data using a template."""
        pass

class TransformerPlugin(BasePlugin):
    """Base class for data transformer plugins."""

    @abstractmethod
    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform documentation data."""
        pass

class StoragePlugin(BasePlugin):
    """Base class for storage plugins."""

    @abstractmethod
    def save(self, data: Dict[str, Any], path: str) -> None:
        """Save documentation data."""
        pass

    @abstractmethod
    def load(self, path: str) -> Dict[str, Any]:
        """Load documentation data."""
        pass

class SearchPlugin(BasePlugin):
    """Base class for search plugins."""

    @abstractmethod
    def index(self, data: Dict[str, Any]) -> None:
        """Index documentation data for searching."""
        pass

    @abstractmethod
    def search(self, query: str) -> Dict[str, Any]:
        """Search indexed documentation."""
        pass
