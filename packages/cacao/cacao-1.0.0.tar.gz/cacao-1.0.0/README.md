# CacaoDocs

A flexible documentation generator with plugin support for Python applications.

## Features

- **Plugin System**: Easily extend functionality with custom plugins
  - Parser plugins for different documentation formats
  - Renderer plugins for custom output formats
  - Data transformer plugins for custom processing
  - Storage plugins for different storage backends
  - Search plugins for enhanced documentation search

- **Built-in Plugins**:
  - Markdown Parser: Parse markdown-formatted documentation
  - HTML Renderer: Generate beautiful HTML documentation
  - OpenAPI Generator: Generate OpenAPI/Swagger specifications

- **Error Handling**:
  - Centralized error management
  - Custom error types and handling
  - Detailed error logging
  - User-friendly error messages

- **Configuration**:
  - YAML-based configuration
  - Customizable themes
  - Plugin configuration support
  - Environment variable support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Basic setup:

```python
from cacao.core.documentation import CacaoDocs

# Initialize CacaoDocs
CacaoDocs.load_config()

# Use the decorator to document API endpoints
@CacaoDocs.doc_api(doc_type="api", tag="users")
def my_endpoint():
    """
    Method: GET
    Version: v1
    Status: Production
    
    Description:
        Example endpoint description.
    
    Responses:
        200:
            description: "Success"
            example: {"status": "ok"}
    """
    pass
```

2. Configuration (cacao.yaml):

```yaml
title: "My API Documentation"
description: "Comprehensive API documentation"
version: "1.0.0"
theme:
  primary_color: "#4CAF50"
  secondary_color: "#8b5d3b"
verbose: true
plugin_directory: "plugins"
```

3. Creating a Custom Plugin:

```python
from cacao.plugins.base_plugin import BasePlugin

class MyCustomPlugin(BasePlugin):
    def initialize(self) -> None:
        # Setup plugin
        pass
        
    def cleanup(self) -> None:
        # Cleanup resources
        pass
```

## Project Structure

```
cacao/
├── core/
│   ├── config.py         # Configuration management
│   ├── documentation.py  # Main CacaoDocs class
│   └── parser.py        # Core documentation parser
├── plugins/
│   ├── base_plugin.py    # Base plugin interfaces
│   ├── plugin_manager.py # Plugin lifecycle management
│   ├── markdown_parser.py # Markdown parsing plugin
│   ├── html_renderer.py  # HTML rendering plugin
│   └── openapi_generator.py # OpenAPI generation plugin
├── templates/
│   └── default.html     # Default HTML template
└── utils/
    └── error_handler.py # Error handling system
```

## Plugin Development

1. Choose a plugin type:
   - ParserPlugin: Parse documentation from different formats
   - RendererPlugin: Generate output in different formats
   - TransformerPlugin: Transform documentation data
   - StoragePlugin: Store documentation in different backends
   - SearchPlugin: Implement custom search functionality

2. Implement the required methods:
   - `initialize()`: Setup plugin resources
   - `cleanup()`: Cleanup plugin resources
   - Plugin-specific methods based on the plugin type

3. Add plugin configuration to cacao.yaml:

```yaml
plugins:
  my_plugin:
    option1: value1
    option2: value2
```

## Error Handling

The error handling system provides:

- Custom exception types for different errors
- Error logging with configurable levels
- Error formatting for API responses
- Error handler decorator for consistent handling

Example:

```python
from cacao.utils.error_handler import ErrorHandler, CacaoDocsError

@ErrorHandler.error_handler("CustomError")
def my_function():
    raise CacaoDocsError("Something went wrong", "CustomError")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
