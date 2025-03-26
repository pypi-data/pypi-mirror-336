"""Markdown parser plugin for CacaoDocs."""
import re
from typing import Dict, Any, List
import markdown2
from bs4 import BeautifulSoup

from .base_plugin import ParserPlugin
from ..utils.error_handler import ErrorHandler

class MarkdownParserPlugin(ParserPlugin):
    """Plugin for parsing markdown documentation."""

    def initialize(self) -> None:
        """Initialize the markdown parser."""
        self.md = markdown2.Markdown(extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'metadata',
            'footnotes'
        ])

    def cleanup(self) -> None:
        """Cleanup resources."""
        pass

    @ErrorHandler.error_handler("ParserError")
    def parse_docstring(self, docstring: str, doc_type: str) -> Dict[str, Any]:
        """
        Parse a markdown docstring into structured data.
        
        Args:
            docstring: The markdown docstring to parse
            doc_type: The type of documentation being parsed
            
        Returns:
            Dict containing parsed metadata and content
        """
        # Convert markdown to HTML
        html = self.md.convert(docstring)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract metadata
        metadata = {
            'title': self._get_title(soup),
            'description': self._get_description(soup),
            'sections': self._get_sections(soup),
            'code_blocks': self._get_code_blocks(soup),
            'tables': self._get_tables(soup)
        }
        
        # Add type-specific parsing
        if doc_type == "api":
            metadata.update(self._parse_api_docs(soup))
        elif doc_type == "types":
            metadata.update(self._parse_type_docs(soup))
            
        return metadata

    def _get_title(self, soup: BeautifulSoup) -> str:
        """Extract title from the first h1 tag."""
        h1 = soup.find('h1')
        return h1.text if h1 else ""

    def _get_description(self, soup: BeautifulSoup) -> str:
        """Extract description from the first paragraph after title."""
        h1 = soup.find('h1')
        if h1 and h1.find_next('p'):
            return h1.find_next('p').text
        return ""

    def _get_sections(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all sections (h2) and their content."""
        sections = {}
        for h2 in soup.find_all('h2'):
            content = []
            for sibling in h2.find_next_siblings():
                if sibling.name == 'h2':
                    break
                content.append(str(sibling))
            sections[h2.text] = ''.join(content)
        return sections

    def _get_code_blocks(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all code blocks with their language."""
        code_blocks = {}
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                lang = code.get('class', [''])[0].replace('language-', '')
                code_blocks[lang or 'text'] = code.text
        return code_blocks

    def _get_tables(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract all tables with headers and rows."""
        tables = []
        for table in soup.find_all('table'):
            headers = []
            rows = []
            
            # Get headers
            thead = table.find('thead')
            if thead:
                headers = [th.text for th in thead.find_all('th')]
            
            # Get rows
            tbody = table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    rows.append([td.text for td in tr.find_all('td')])
            
            tables.append({
                'headers': headers,
                'rows': rows
            })
        
        return tables

    def _parse_api_docs(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract API-specific metadata."""
        metadata = {}
        
        # Look for common API doc patterns
        endpoint = re.search(r'Endpoint:\s*(.+)', soup.text)
        if endpoint:
            metadata['endpoint'] = endpoint.group(1).strip()
            
        method = re.search(r'Method:\s*(.+)', soup.text)
        if method:
            metadata['method'] = method.group(1).strip()
            
        # Extract parameters
        params_section = None
        for h3 in soup.find_all('h3'):
            if 'Parameters' in h3.text:
                params_section = h3
                break
                
        if params_section:
            params = []
            table = params_section.find_next('table')
            if table:
                for row in table.find_all('tr')[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        params.append({
                            'name': cols[0].text.strip(),
                            'type': cols[1].text.strip(),
                            'description': cols[2].text.strip()
                        })
            metadata['parameters'] = params
            
        return metadata

    def _parse_type_docs(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract type definition metadata."""
        metadata = {}
        
        # Look for type definition patterns
        type_def = re.search(r'Type:\s*(.+)', soup.text)
        if type_def:
            metadata['type_name'] = type_def.group(1).strip()
            
        # Extract properties
        props_section = None
        for h3 in soup.find_all('h3'):
            if 'Properties' in h3.text:
                props_section = h3
                break
                
        if props_section:
            properties = []
            table = props_section.find_next('table')
            if table:
                for row in table.find_all('tr')[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        properties.append({
                            'name': cols[0].text.strip(),
                            'type': cols[1].text.strip(),
                            'description': cols[2].text.strip()
                        })
            metadata['properties'] = properties
            
        return metadata
