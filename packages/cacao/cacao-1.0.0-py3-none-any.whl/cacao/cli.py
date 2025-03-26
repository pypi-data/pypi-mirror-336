"""Command-line interface for CacaoDocs."""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .core.documentation import CacaoDocs
from .core.config import Config
from .utils.error_handler import ErrorHandler, CacaoDocsError
from .plugins.plugin_manager import PluginManager

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CacaoDocs - A flexible documentation generator with plugin support"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (default: cacao.yaml)",
        default="cacao.yaml"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate documentation")
    generate_parser.add_argument(
        "--output",
        type=str,
        help="Output directory (default: docs)",
        default="docs"
    )
    generate_parser.add_argument(
        "--format",
        type=str,
        choices=["html", "json", "openapi"],
        help="Output format (default: html)",
        default="html"
    )
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start documentation server")
    serve_parser.add_argument(
        "--host",
        type=str,
        help="Host to serve on (default: 127.0.0.1)",
        default="127.0.0.1"
    )
    serve_parser.add_argument(
        "--port",
        type=int,
        help="Port to serve on (default: 5000)",
        default=5000
    )
    
    # Plugin commands
    plugin_parser = subparsers.add_parser("plugin", help="Plugin management")
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_command", help="Plugin commands")
    
    # List plugins
    plugin_subparsers.add_parser("list", help="List available plugins")
    
    # Enable plugin
    enable_parser = plugin_subparsers.add_parser("enable", help="Enable a plugin")
    enable_parser.add_argument("name", help="Plugin name")
    
    # Disable plugin
    disable_parser = plugin_subparsers.add_parser("disable", help="Disable a plugin")
    disable_parser.add_argument("name", help="Plugin name")
    
    return parser.parse_args(args)

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    try:
        parsed_args = parse_args(args)
        
        # Set verbose mode if requested
        if parsed_args.verbose:
            Config.configure(verbose=True)
            ErrorHandler.setup_logging()
        
        # Load configuration
        CacaoDocs.load_config(parsed_args.config)
        
        if parsed_args.command == "generate":
            output_dir = Path(parsed_args.output)
            
            if parsed_args.format == "html":
                # Generate HTML documentation
                html = CacaoDocs.get_html()
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "index.html").write_text(html)
                print(f"Generated HTML documentation in {output_dir}")
                
            elif parsed_args.format == "json":
                # Generate JSON documentation
                json_data = CacaoDocs.get_json()
                output_dir.mkdir(parents=True, exist_ok=True)
                import json
                (output_dir / "docs.json").write_text(
                    json.dumps(json_data, indent=2)
                )
                print(f"Generated JSON documentation in {output_dir}")
                
            elif parsed_args.format == "openapi":
                # Generate OpenAPI documentation using the plugin
                openapi_plugins = PluginManager.get_plugins_by_type("OpenAPIGeneratorPlugin")
                if not openapi_plugins:
                    raise CacaoDocsError("OpenAPI generator plugin not found")
                    
                plugin = openapi_plugins[0]
                spec = plugin.generate_openapi(CacaoDocs.get_json().get("api", []))
                output_dir.mkdir(parents=True, exist_ok=True)
                plugin.save_openapi_spec(str(output_dir / "openapi.yaml"))
                print(f"Generated OpenAPI documentation in {output_dir}")
                
        elif parsed_args.command == "serve":
            # Start documentation server
            from flask import Flask
            app = Flask(__name__)
            app = CacaoDocs.create_app(app)
            print(f"Starting documentation server at http://{parsed_args.host}:{parsed_args.port}")
            app.run(host=parsed_args.host, port=parsed_args.port)
            
        elif parsed_args.command == "plugin":
            if parsed_args.plugin_command == "list":
                # List available plugins
                plugins = PluginManager.get_all_plugins()
                if plugins:
                    print("\nAvailable plugins:")
                    for name, plugin in plugins.items():
                        enabled = "enabled" if Config.get(f"plugins.{name}.enabled", True) else "disabled"
                        print(f"  - {name} ({enabled})")
                else:
                    print("No plugins available")
                    
            elif parsed_args.plugin_command == "enable":
                # Enable plugin
                config = Config.get_all()
                if "plugins" not in config:
                    config["plugins"] = {}
                if parsed_args.name not in config["plugins"]:
                    config["plugins"][parsed_args.name] = {}
                config["plugins"][parsed_args.name]["enabled"] = True
                Config.set("plugins", config["plugins"])
                print(f"Enabled plugin: {parsed_args.name}")
                
            elif parsed_args.plugin_command == "disable":
                # Disable plugin
                config = Config.get_all()
                if "plugins" in config and parsed_args.name in config["plugins"]:
                    config["plugins"][parsed_args.name]["enabled"] = False
                    Config.set("plugins", config["plugins"])
                    print(f"Disabled plugin: {parsed_args.name}")
                else:
                    print(f"Plugin not found: {parsed_args.name}")
                    
        else:
            print("No command specified. Use --help for usage information.")
            return 1
            
        return 0
        
    except Exception as e:
        if isinstance(e, CacaoDocsError):
            print(f"Error: {e.message}")
        else:
            print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
