"""OpenAPI documentation generator plugin for CacaoDocs."""
from typing import Dict, Any, List
import yaml
import re
from pathlib import Path

from .base_plugin import BasePlugin
from ..utils.error_handler import ErrorHandler

class OpenAPIGeneratorPlugin(BasePlugin):
    """Plugin for generating OpenAPI/Swagger documentation."""

    def initialize(self) -> None:
        """Initialize the OpenAPI generator."""
        self.openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "API Documentation",
                "version": "1.0.0"
            },
            "paths": {},
            "components": {
                "schemas": {},
                "responses": {},
                "parameters": {},
                "examples": {}
            }
        }

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.openapi_spec = None

    @ErrorHandler.error_handler()
    def generate_openapi(self, api_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate OpenAPI specification from API documentation."""
        # Update info from config
        self.openapi_spec["info"]["title"] = self.get_config("title", "API Documentation")
        self.openapi_spec["info"]["version"] = self.get_config("version", "1.0.0")
        self.openapi_spec["info"]["description"] = self.get_config("description", "")

        # Process each API endpoint
        for doc in api_docs:
            self._process_endpoint(doc)

        return self.openapi_spec

    def _process_endpoint(self, doc: Dict[str, Any]) -> None:
        """Process a single API endpoint."""
        endpoint = doc.get("endpoint")
        if not endpoint:
            return

        method = doc.get("method", "get").lower()
        
        # Initialize path if not exists
        if endpoint not in self.openapi_spec["paths"]:
            self.openapi_spec["paths"][endpoint] = {}

        # Build operation object
        operation = {
            "summary": doc.get("description", ""),
            "tags": [doc.get("tag", "general")],
            "parameters": self._build_parameters(doc),
            "responses": self._build_responses(doc)
        }

        # Add request body if method supports it
        if method in ["post", "put", "patch"]:
            request_body = self._build_request_body(doc)
            if request_body:
                operation["requestBody"] = request_body

        # Add operation to path
        self.openapi_spec["paths"][endpoint][method] = operation

    def _build_parameters(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build OpenAPI parameters from documentation."""
        parameters = []
        
        # Path parameters
        path_params = re.findall(r'<(\w+:)?(\w+)>', doc.get("endpoint", ""))
        for _, param_name in path_params:
            param = {
                "name": param_name,
                "in": "path",
                "required": True,
                "schema": {"type": "string"}
            }
            parameters.append(param)

        # Query parameters from args
        for name, details in doc.get("args", {}).items():
            if name not in [p["name"] for p in parameters]:  # Skip if already added
                param = {
                    "name": name,
                    "in": "query",
                    "description": details.get("description", ""),
                    "schema": self._get_schema_for_type(details.get("type", "string"))
                }
                parameters.append(param)

        return parameters

    def _build_responses(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Build OpenAPI responses from documentation."""
        responses = {}
        
        for status, details in doc.get("responses", {}).items():
            response = {
                "description": details.get("description", ""),
            }
            
            if "example" in details:
                try:
                    # Try to parse example as JSON/dict
                    if isinstance(details["example"], str):
                        import json
                        example = json.loads(details["example"])
                    else:
                        example = details["example"]
                    
                    response["content"] = {
                        "application/json": {
                            "schema": self._infer_schema(example),
                            "example": example
                        }
                    }
                except Exception:
                    # If not JSON, treat as plain text
                    response["content"] = {
                        "text/plain": {
                            "example": details["example"]
                        }
                    }
            
            responses[str(status)] = response
            
        return responses

    def _build_request_body(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Build OpenAPI request body from documentation."""
        if "json_body" in doc:
            return {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": self._get_schema_for_type(doc["json_body"].get("type", "object")),
                        "example": doc["json_body"].get("example")
                    }
                }
            }
        return None

    def _get_schema_for_type(self, type_str: str) -> Dict[str, Any]:
        """Convert Python type string to OpenAPI schema."""
        type_map = {
            "str": {"type": "string"},
            "int": {"type": "integer"},
            "float": {"type": "number"},
            "bool": {"type": "boolean"},
            "list": {"type": "array", "items": {}},
            "dict": {"type": "object"},
            "object": {"type": "object"}
        }
        
        # Handle array types (e.g., "List[str]")
        if type_str.startswith(("list[", "List[")):
            item_type = re.search(r'\[(.*?)\]', type_str).group(1).lower()
            return {
                "type": "array",
                "items": type_map.get(item_type, {"type": "string"})
            }
            
        return type_map.get(type_str.lower(), {"type": "string"})

    def _infer_schema(self, example: Any) -> Dict[str, Any]:
        """Infer OpenAPI schema from example value."""
        if isinstance(example, dict):
            properties = {}
            for key, value in example.items():
                properties[key] = self._infer_schema(value)
            return {
                "type": "object",
                "properties": properties
            }
        elif isinstance(example, list):
            if example:
                return {
                    "type": "array",
                    "items": self._infer_schema(example[0])
                }
            return {
                "type": "array",
                "items": {}
            }
        elif isinstance(example, bool):
            return {"type": "boolean"}
        elif isinstance(example, int):
            return {"type": "integer"}
        elif isinstance(example, float):
            return {"type": "number"}
        else:
            return {"type": "string"}

    @ErrorHandler.error_handler()
    def save_openapi_spec(self, output_path: str) -> None:
        """Save OpenAPI specification to a file."""
        with open(output_path, 'w') as f:
            yaml.dump(self.openapi_spec, f, sort_keys=False)
