"""Plugin system for CacaoDocs."""

from .base_plugin import (
    BasePlugin,
    ParserPlugin,
    RendererPlugin,
    TransformerPlugin,
    StoragePlugin,
    SearchPlugin
)
from .plugin_manager import PluginManager
from .markdown_parser import MarkdownParserPlugin
from .html_renderer import HTMLRendererPlugin
from .openapi_generator import OpenAPIGeneratorPlugin

# Register built-in plugins
PluginManager.register_plugin_type("parser", ParserPlugin)
PluginManager.register_plugin_type("renderer", RendererPlugin)
PluginManager.register_plugin_type("transformer", TransformerPlugin)
PluginManager.register_plugin_type("storage", StoragePlugin)
PluginManager.register_plugin_type("search", SearchPlugin)

# Initialize built-in plugins
PluginManager.load_plugin("cacaodocs.plugins.html_renderer", {
    "enabled": True,
    "template": "default",
    "syntax_highlighting": True
})

PluginManager.load_plugin("cacaodocs.plugins.markdown_parser", {
    "enabled": True,
    "extensions": [
        "fenced-code-blocks",
        "tables",
        "header-ids",
        "metadata",
        "footnotes"
    ]
})

PluginManager.load_plugin("cacaodocs.plugins.openapi_generator", {
    "enabled": True,
    "output_format": "yaml",
    "include_examples": True
})

__all__ = [
    "BasePlugin",
    "ParserPlugin",
    "RendererPlugin",
    "TransformerPlugin",
    "StoragePlugin",
    "SearchPlugin",
    "PluginManager",
    "MarkdownParserPlugin",
    "HTMLRendererPlugin",
    "OpenAPIGeneratorPlugin"
]
