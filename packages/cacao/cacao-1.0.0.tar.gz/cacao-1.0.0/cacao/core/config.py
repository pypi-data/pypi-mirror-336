"""Configuration management for CacaoDocs."""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Handles configuration loading and management."""
    
    _instance = None
    _config: Dict[str, Any] = {
        "title": "Welcome to CacaoDocs Dashboard",
        "description": "Manage and explore your documentation with ease",
        "version": "1.0.0",
        "theme": {
            "primary_color": "#4CAF50",
            "secondary_color": "#8b5d3b",
            "background_color": "#f5f5f5",
            "text_color": "#331201",
            "sidebar_background_color": "#ffffff",
            "sidebar_text_color": "#331201",
            "sidebar_highlight_background_color": "#736d67",
            "sidebar_highlight_text_color": "#ffffff",
            "highlight_code_background_color": "#3a2f2a",
            "highlight_code_border_color": "#8b5d3b"
        },
        "type_mappings": {
            "api": "API",
            "types": "Types",
            "docs": "Documentation"
        },
        "tag_mappings": {},
        "logo_url": "cacaodocs/templates/assets/img/logo.png",
        "verbose": False,
        "exclude_inputs": ["self"]
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> None:
        """Load configuration from a YAML file."""
        if config_path is None:
            config_path = Path.cwd() / 'cacao.yaml'
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    cls._config.update(config)
        except FileNotFoundError:
            pass  # Use default config
        except yaml.YAMLError as e:
            from ..utils.error_handler import ErrorHandler
            ErrorHandler.handle_error("ConfigError", f"Error parsing configuration file: {e}")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return cls._config.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """Set a configuration value."""
        cls._config[key] = value

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get the entire configuration dictionary."""
        return cls._config.copy()
