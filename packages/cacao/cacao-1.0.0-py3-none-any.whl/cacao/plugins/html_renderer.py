"""HTML renderer plugin for CacaoDocs."""
from typing import Dict, Any
import jinja2
import os
from pathlib import Path

from .base_plugin import RendererPlugin
from ..utils.error_handler import ErrorHandler

class HTMLRendererPlugin(RendererPlugin):
    """Plugin for rendering documentation as HTML."""

    def initialize(self) -> None:
        """Initialize the HTML renderer."""
        template_dir = Path(__file__).parent.parent / 'templates'
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['format_type'] = self._format_type
        self.env.filters['format_code'] = self._format_code

    def cleanup(self) -> None:
        """Cleanup resources."""
        pass

    @ErrorHandler.error_handler("RenderError")
    def render(self, data: Dict[str, Any], template: str = "default") -> str:
        """
        Render documentation data using a template.
        
        Args:
            data: Documentation data to render
            template: Template name to use (default uses base template)
            
        Returns:
            Rendered HTML string
        """
        # Load template
        template_name = f"{template}.html"
        template = self.env.get_template(template_name)
        
        # Prepare data for rendering
        render_data = self._prepare_data(data)
        
        # Render template
        return template.render(**render_data)

    def _prepare_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for rendering."""
        render_data = {
            'title': data.get('configs', {}).get('title', 'CacaoDocs'),
            'description': data.get('configs', {}).get('description', ''),
            'version': data.get('configs', {}).get('version', '1.0.0'),
            'theme': data.get('configs', {}).get('theme', {}),
            'api_docs': self._prepare_api_docs(data.get('api', [])),
            'type_docs': self._prepare_type_docs(data.get('types', [])),
            'general_docs': self._prepare_general_docs(data.get('docs', []))
        }
        return render_data

    def _prepare_api_docs(self, api_docs: list) -> list:
        """Prepare API documentation for rendering."""
        prepared = []
        for doc in api_docs:
            prepared.append({
                'name': doc.get('function_name', ''),
                'endpoint': doc.get('endpoint', ''),
                'method': doc.get('method', ''),
                'description': doc.get('description', ''),
                'parameters': doc.get('args', {}),
                'responses': doc.get('responses', {}),
                'source': self._format_code(doc.get('function_source', '')),
                'status': doc.get('status', 'Unknown'),
                'version': doc.get('version', '1.0.0'),
                'tag': doc.get('tag', 'general')
            })
        return prepared

    def _prepare_type_docs(self, type_docs: list) -> list:
        """Prepare type documentation for rendering."""
        prepared = []
        for doc in type_docs:
            prepared.append({
                'name': doc.get('name', ''),
                'description': doc.get('description', ''),
                'properties': doc.get('properties', {}),
                'methods': doc.get('methods', {}),
                'source': self._format_code(doc.get('source', '')),
                'examples': doc.get('examples', [])
            })
        return prepared

    def _prepare_general_docs(self, docs: list) -> list:
        """Prepare general documentation for rendering."""
        prepared = []
        for doc in docs:
            prepared.append({
                'title': doc.get('title', ''),
                'content': doc.get('content', ''),
                'sections': doc.get('sections', {}),
                'tag': doc.get('tag', 'general')
            })
        return prepared

    def _format_type(self, type_str: str) -> str:
        """Format a type string for display."""
        if not type_str:
            return 'any'
        return type_str.replace('typing.', '')

    def _format_code(self, code: str) -> str:
        """Format code for display."""
        if not code:
            return ''
        # Here you could add syntax highlighting
        return code.strip()
