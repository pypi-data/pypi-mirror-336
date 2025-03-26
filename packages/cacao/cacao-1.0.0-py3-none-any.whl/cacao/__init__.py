"""Cacao - A flexible documentation generator with plugin support."""

from .core.documentation import CacaoDocs
from .core.config import Config
from .utils.error_handler import ErrorHandler, CacaoDocsError
from .plugins.plugin_manager import PluginManager
from .plugins.base_plugin import (
    BasePlugin,
    ParserPlugin,
    RendererPlugin,
    TransformerPlugin,
    StoragePlugin,
    SearchPlugin
)

__version__ = "1.0.0"

__all__ = [
    "CacaoDocs",
    "Config",
    "ErrorHandler",
    "CacaoDocsError",
    "PluginManager",
    "BasePlugin",
    "ParserPlugin",
    "RendererPlugin",
    "TransformerPlugin",
    "StoragePlugin",
    "SearchPlugin",
]
