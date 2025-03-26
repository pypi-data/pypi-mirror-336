"""Plugin management system for CacaoDocs."""
import importlib
import inspect
from typing import Dict, Type, List, Any, Optional
from pathlib import Path

from .base_plugin import BasePlugin
from ..utils.error_handler import ErrorHandler, PluginError
from ..core.config import Config

class PluginManager:
    """Manages CacaoDocs plugins lifecycle and operations."""

    _instance = None
    _plugins: Dict[str, BasePlugin] = {}
    _plugin_types: Dict[str, Type[BasePlugin]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PluginManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register_plugin_type(cls, name: str, plugin_type: Type[BasePlugin]) -> None:
        """Register a new plugin type."""
        cls._plugin_types[name] = plugin_type

    @classmethod
    @ErrorHandler.error_handler("PluginError")
    def load_plugin(cls, plugin_path: str, config: Dict[str, Any] = None) -> None:
        """
        Load a plugin from a Python module.
        
        Args:
            plugin_path: Import path to the plugin module (e.g., 'cacaodocs.plugins.html_renderer')
            config: Optional configuration for the plugin
        """
        try:
            # Import the module
            module = importlib.import_module(plugin_path)
            
            # Find plugin class in the module
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and issubclass(obj, BasePlugin) 
                    and obj != BasePlugin and not inspect.isabstract(obj)):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                raise PluginError(f"No valid plugin class found in {plugin_path}")
            
            # Create and initialize plugin instance
            plugin = plugin_class(config)
            plugin.initialize()
            
            # Register plugin
            cls._plugins[plugin.name] = plugin
            
            # Update config
            plugins_config = Config.get("plugins", {})
            if plugin_path not in plugins_config:
                plugins_config[plugin_path] = {"enabled": True}
                Config.set("plugins", plugins_config)
                
        except ImportError as e:
            raise PluginError(f"Failed to import plugin {plugin_path}: {str(e)}")
        except Exception as e:
            raise PluginError(f"Error loading plugin {plugin_path}: {str(e)}")

    @classmethod
    @ErrorHandler.error_handler("PluginError")
    def unload_plugin(cls, plugin_name: str) -> None:
        """Unload and cleanup a plugin."""
        if plugin_name not in cls._plugins:
            raise PluginError(f"Plugin {plugin_name} not found")
        
        try:
            plugin = cls._plugins[plugin_name]
            plugin.cleanup()
            del cls._plugins[plugin_name]
            
            # Update config
            plugins_config = Config.get("plugins", {})
            if plugin_name in plugins_config:
                plugins_config[plugin_name]["enabled"] = False
                Config.set("plugins", plugins_config)
                
        except Exception as e:
            raise PluginError(f"Error unloading plugin {plugin_name}: {str(e)}")

    @classmethod
    def get_plugin(cls, plugin_name: str) -> Optional[BasePlugin]:
        """Get a loaded plugin by name."""
        return cls._plugins.get(plugin_name)

    @classmethod
    def get_plugins_by_type(cls, plugin_type: Type[BasePlugin]) -> List[BasePlugin]:
        """Get all loaded plugins of a specific type."""
        return [p for p in cls._plugins.values() if isinstance(p, plugin_type)]

    @classmethod
    def get_all_plugins(cls) -> Dict[str, BasePlugin]:
        """Get all loaded plugins."""
        return cls._plugins.copy()

    @classmethod
    @ErrorHandler.error_handler("PluginError")
    def load_plugins_from_directory(cls, directory: str) -> None:
        """
        Load all plugins from a directory.
        
        Args:
            directory: Path to directory containing plugin modules
        """
        plugin_dir = Path(directory)
        if not plugin_dir.exists() or not plugin_dir.is_dir():
            raise PluginError(f"Plugin directory {directory} not found")
        
        # Get the package name from the directory path
        package_name = plugin_dir.parent.name
        
        for plugin_file in plugin_dir.glob("*.py"):
            if plugin_file.stem != "__init__":
                plugin_path = f"{package_name}.plugins.{plugin_file.stem}"
                cls.load_plugin(plugin_path)

    @classmethod
    def reload_all_plugins(cls) -> None:
        """Reload all currently loaded plugins."""
        plugins = list(cls._plugins.keys())
        for plugin_name in plugins:
            cls.unload_plugin(plugin_name)
            cls.load_plugin(plugin_name)

    @classmethod
    def cleanup(cls) -> None:
        """Cleanup all plugins."""
        for plugin_name in list(cls._plugins.keys()):
            cls.unload_plugin(plugin_name)
