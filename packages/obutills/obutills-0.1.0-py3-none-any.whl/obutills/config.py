"""
Configuration utilities for Python applications.
"""

import os
import json
import yaml
import configparser
from typing import Dict, Any, Optional, Union, List
from pathlib import Path


class ConfigManager:
    """
    A unified configuration manager that supports multiple formats
    (JSON, YAML, INI) and environment variables.
    """
    
    def __init__(self, 
                config_file: Optional[str] = None, 
                env_prefix: str = "",
                default_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str, optional): Path to the configuration file
            env_prefix (str): Prefix for environment variables
            default_config (dict, optional): Default configuration values
        """
        self.config_file = config_file
        self.env_prefix = env_prefix
        self.config = default_config or {}
        
        if config_file:
            self.load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        for key, value in os.environ.items():
            if self.env_prefix and not key.startswith(self.env_prefix):
                continue
                
            # Remove prefix if it exists
            if self.env_prefix:
                config_key = key[len(self.env_prefix):]
            else:
                config_key = key
                
            # Convert nested keys (e.g., "DATABASE_URL" -> ["DATABASE", "URL"])
            if "_" in config_key:
                parts = config_key.lower().split("_")
                
                # Navigate to the correct nested dictionary
                current = self.config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    elif not isinstance(current[part], dict):
                        # If it's not a dict, make it one and preserve the old value
                        current[part] = {"value": current[part]}
                    current = current[part]
                
                # Set the value
                current[parts[-1]] = self._parse_env_value(value)
            else:
                self.config[config_key.lower()] = self._parse_env_value(value)
    
    @staticmethod
    def _parse_env_value(value: str) -> Union[str, int, float, bool, List, Dict]:
        """
        Parse environment variable values into appropriate Python types.
        
        Args:
            value (str): The string value from the environment variable
            
        Returns:
            The parsed value as the appropriate type
        """
        # Check for boolean values
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
        
        # Check for numeric values
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Check for JSON values (lists, dicts)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        
        # Default to string
        return value
    
    def load_from_file(self, file_path: str) -> None:
        """
        Load configuration from a file.
        
        Args:
            file_path (str): Path to the configuration file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in (".json", ".jsn"):
            with open(file_path, "r") as f:
                self.config.update(json.load(f))
        
        elif file_ext in (".yaml", ".yml"):
            with open(file_path, "r") as f:
                self.config.update(yaml.safe_load(f))
        
        elif file_ext in (".ini", ".cfg", ".conf"):
            parser = configparser.ConfigParser()
            parser.read(file_path)
            
            # Convert ConfigParser object to dictionary
            for section in parser.sections():
                self.config[section] = {}
                for key, value in parser[section].items():
                    self.config[section][key] = self._parse_env_value(value)
        
        else:
            raise ValueError(f"Unsupported configuration file format: {file_ext}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key (can use dot notation for nested values)
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default
        """
        parts = key.split(".")
        current = self.config
        
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
        
        return current
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key (can use dot notation for nested values)
            value: Value to set
        """
        parts = key.split(".")
        current = self.config
        
        # Navigate to the correct nested dictionary
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the value
        current[parts[-1]] = value
    
    def save(self, file_path: Optional[str] = None) -> None:
        """
        Save the configuration to a file.
        
        Args:
            file_path (str, optional): Path to save to (defaults to the original file)
            
        Raises:
            ValueError: If no file path is provided and no original file exists
        """
        file_path = file_path or self.config_file
        if not file_path:
            raise ValueError("No file path provided for saving configuration")
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in (".json", ".jsn"):
            with open(file_path, "w") as f:
                json.dump(self.config, f, indent=2)
        
        elif file_ext in (".yaml", ".yml"):
            with open(file_path, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False)
        
        elif file_ext in (".ini", ".cfg", ".conf"):
            parser = configparser.ConfigParser()
            
            # Convert dictionary to ConfigParser object
            for section, values in self.config.items():
                if not isinstance(values, dict):
                    # Handle top-level non-dict values
                    if "DEFAULT" not in parser:
                        parser["DEFAULT"] = {}
                    parser["DEFAULT"][section] = str(values)
                    continue
                
                parser[section] = {}
                for key, value in values.items():
                    parser[section][key] = str(value)
            
            with open(file_path, "w") as f:
                parser.write(f)
        
        else:
            raise ValueError(f"Unsupported configuration file format: {file_ext}")
        
        # Update the config file path
        self.config_file = file_path
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-like access to configuration values."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-like setting of configuration values."""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the configuration."""
        return self.get(key) is not None


def load_config(file_path: str, env_prefix: str = "") -> ConfigManager:
    """
    Convenience function to load configuration from a file.
    
    Args:
        file_path (str): Path to the configuration file
        env_prefix (str): Prefix for environment variables
        
    Returns:
        ConfigManager: A configuration manager instance
    """
    return ConfigManager(file_path, env_prefix)


def get_app_config_dir(app_name: str, create: bool = True) -> str:
    """
    Get the platform-specific application configuration directory.
    
    Args:
        app_name (str): Name of the application
        create (bool): Whether to create the directory if it doesn't exist
        
    Returns:
        str: Path to the application configuration directory
    """
    # Determine the base config directory based on platform
    if os.name == "nt":  # Windows
        base_dir = os.path.join(os.environ.get("APPDATA", ""), app_name)
    elif os.name == "posix":  # Linux, macOS, etc.
        # Use XDG_CONFIG_HOME if available, otherwise ~/.config
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            base_dir = os.path.join(xdg_config, app_name)
        else:
            base_dir = os.path.join(os.path.expanduser("~"), ".config", app_name)
    else:
        # Fallback for other platforms
        base_dir = os.path.join(os.path.expanduser("~"), f".{app_name}")
    
    # Create the directory if requested
    if create and not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    return base_dir
