"""Main CacaoDocs class with plugin support and error handling."""
import inspect
from typing import Dict, Any, Optional, List
from pathlib import Path
from flask import Flask, jsonify

from .config import Config
from .parser import Parser
from ..utils.error_handler import ErrorHandler, CacaoDocsError
from ..plugins.plugin_manager import PluginManager
from ..plugins.base_plugin import (
    RendererPlugin,
    ParserPlugin,
    BasePlugin,
    TransformerPlugin,
    StoragePlugin,
    SearchPlugin
)
from ..plugins.html_renderer import HTMLRendererPlugin
from ..plugins.markdown_parser import MarkdownParserPlugin
from ..plugins.openapi_generator import OpenAPIGeneratorPlugin

class CacaoDocs:
    """Main class for handling documentation with plugin support."""

    _registry = {
        'api': [],
        'types': [],
        'docs': []
    }

    @classmethod
    @ErrorHandler.error_handler("ConfigError")
    def load_config(cls, config_path: Optional[str] = None) -> None:
        """Load configuration and initialize components."""
        # Load configuration
        Config.load_config(config_path)

        # Setup error handling
        if Config.get("verbose"):
            ErrorHandler.setup_logging()

        # Initialize built-in plugins
        html_config = Config.get("plugins", {}).get("html_renderer", {})
        markdown_config = Config.get("plugins", {}).get("markdown_parser", {})
        openapi_config = Config.get("plugins", {}).get("openapi_generator", {})

        # Register plugin types
        PluginManager.register_plugin_type("renderer", RendererPlugin)
        PluginManager.register_plugin_type("parser", ParserPlugin)
        PluginManager.register_plugin_type("transformer", TransformerPlugin)
        PluginManager.register_plugin_type("storage", StoragePlugin)
        PluginManager.register_plugin_type("search", SearchPlugin)

        # Initialize built-in plugins
        plugin_dir = Path("cacaodocs/plugins")
        if plugin_dir.exists():
            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.stem not in ["__init__", "base_plugin", "plugin_manager"]:
                    plugin_path = f"cacaodocs.plugins.{plugin_file.stem}"
                    try:
                        PluginManager.load_plugin(plugin_path)
                    except Exception as e:
                        if Config.get("verbose"):
                            print(f"Failed to load plugin {plugin_path}: {e}")

        # Initialize parser
        Parser.initialize()

    @classmethod
    @ErrorHandler.error_handler()
    def doc_api(cls, doc_type: str = "api", tag: str = "general"):
        """
        Decorator for capturing and storing documentation metadata.

        Args:
            doc_type (str): Type of documentation ('api', 'types', 'docs')
            tag (str): Tag for grouping related items
        """
        def decorator(func):
            # Get docstring and parse it
            docstring = func.__doc__ or ""
            metadata = Parser.parse_docstring(docstring, doc_type)

            # Build metadata dictionary
            doc_data = {
                "function_name": func.__name__,
                "tag": tag,
                "type": doc_type
            }
            doc_data.update(metadata)

            # Get source code
            try:
                source = inspect.getsource(func)
                doc_data["function_source"] = source
            except Exception:
                doc_data["function_source"] = None

            # Get signature info
            signature = inspect.signature(func)
            exclude = Config.get("exclude_inputs", [])
            doc_data["inputs"] = [p for p in signature.parameters.keys() if p not in exclude]
            
            return_annotation = signature.return_annotation
            doc_data["outputs"] = (
                str(return_annotation) if return_annotation is not inspect.Signature.empty else None
            )

            # Register documentation
            if doc_type in cls._registry:
                cls._registry[doc_type].append(doc_data)
            else:
                cls._registry['docs'].append(doc_data)

            return func
        return decorator

    @classmethod
    def get_json(cls) -> Dict[str, Any]:
        """Get documentation data as JSON."""
        return {
            **cls._registry,
            "configs": Config.get_all()
        }

    @classmethod
    @ErrorHandler.error_handler()
    def get_html(cls) -> str:
        """Get documentation as HTML using available renderer plugins."""
        data = cls.get_json()
        
        # Try each renderer plugin
        renderer_plugins = PluginManager.get_plugins_by_type(RendererPlugin)
        if not renderer_plugins:
            raise CacaoDocsError("No renderer plugins available")
            
        for plugin in renderer_plugins:
            try:
                result = plugin.render(data, "default")
                if result:
                    return result
            except Exception as e:
                if Config.get("verbose"):
                    print(f"Renderer plugin {plugin.name} failed: {e}")
                continue
        
        # If all plugins failed, raise error
        raise CacaoDocsError("All renderer plugins failed")

    @classmethod
    def create_app(cls, app: Optional[Flask] = None) -> Flask:
        """Create or configure Flask application with documentation routes."""
        if app is None:
            app = Flask(__name__)

        @app.route('/docs/json')
        def get_documentation():
            """Get documentation data as JSON."""
            try:
                documentation = cls.get_json()
                response = jsonify(documentation)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 200
            except Exception as e:
                error = ErrorHandler.format_error(e)
                return jsonify(error), 500

        @app.route('/docs')
        def get_documentation_html():
            """Get documentation as HTML."""
            try:
                html = cls.get_html()
                return html, 200, {'Content-Type': 'text/html'}
            except Exception as e:
                error = ErrorHandler.format_error(e)
                return jsonify(error), 500

        @app.route('/docs/types')
        def get_type_definitions():
            """Get type definitions."""
            try:
                types = cls._registry.get('types', [])
                response = jsonify(types)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 200
            except Exception as e:
                error = ErrorHandler.format_error(e)
                return jsonify(error), 500

        @app.route('/docs/api')
        def get_api_docs():
            """Get API documentation."""
            try:
                api_docs = cls._registry.get('api', [])
                response = jsonify(api_docs)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response, 200
            except Exception as e:
                error = ErrorHandler.format_error(e)
                return jsonify(error), 500

        @app.errorhandler(404)
        def not_found(e):
            """Handle 404 errors."""
            return jsonify(ErrorHandler.format_error(
                CacaoDocsError("Resource not found", "NotFoundError")
            )), 404

        @app.errorhandler(500)
        def server_error(e):
            """Handle 500 errors."""
            return jsonify(ErrorHandler.format_error(
                CacaoDocsError("Internal server error", "ServerError")
            )), 500

        return app
