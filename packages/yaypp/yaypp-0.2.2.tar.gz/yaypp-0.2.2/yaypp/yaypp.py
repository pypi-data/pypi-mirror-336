from typing import Dict, Any, TextIO, Optional
import yaml

class Yaypp:
    def __init__(self, indent: int = 2, width: int = 80, allow_unicode: bool = True,
                 explicit_start: bool = False, explicit_end: bool = False, sort_keys: bool = False,
                 default_style: Optional[str] = None, default_flow_style: bool = False,
                 line_break: Optional[str] = None, encoding: Optional[str] = None,
                 tags: Optional[Dict] = None, version: Optional[tuple] = None,
                 canonical: bool = False):
        """
        Initialize YAML Pretty Printer.
        
        Args:
            indent (int): Number of spaces to use for indentation
            width (int): Maximum line width before wrapping
            allow_unicode (bool): Allow unicode characters in output
            explicit_start (bool): Add explicit document start marker (---)
            explicit_end (bool): Add explicit document end marker (...)
            sort_keys (bool): Sort dictionary keys alphabetically
            default_style (str): Default scalar style ('' or None, '|', '>', '"', "'")
            default_flow_style (bool): Use flow style for collections
            line_break (str): Line break style ('\n', '\r', or '\r\n')
            encoding (str): Character encoding for output
            tags (dict): Custom tag definitions
            version (tuple): YAML version to use (e.g. (1,1) or (1,2))
            canonical (bool): Write "canonical" YAML form
            allow_duplicate_keys (bool): Allow duplicate keys in mappings
        """
        self.indent = indent
        self.width = width
        self.allow_unicode = allow_unicode
        self.explicit_start = explicit_start
        self.explicit_end = explicit_end
        self.sort_keys = sort_keys
        self.default_style = default_style
        self.default_flow_style = default_flow_style
        self.line_break = line_break
        self.encoding = encoding
        self.tags = tags
        self.version = version
        self.canonical = canonical

    def format_yaml(self, yaml_str: str) -> str:
        """
        Format YAML string with consistent indentation and spacing.
        
        Args:
            yaml_str (str): Input YAML string
            
        Returns:
            str: Formatted YAML string
        """
        # Parse YAML into Python object
        data = yaml.safe_load(yaml_str)
        
        # Dump back to YAML with consistent formatting
        return yaml.dump(data,
                        default_flow_style=self.default_flow_style,
                        default_style=self.default_style,
                        allow_unicode=self.allow_unicode,
                        indent=self.indent,
                        width=self.width,
                        explicit_start=self.explicit_start,
                        explicit_end=self.explicit_end,
                        sort_keys=self.sort_keys,
                        encoding=self.encoding,
                        line_break=self.line_break,
                        tags=self.tags,
                        version=self.version,
                        canonical=self.canonical)

    def format_file(self, input_file: TextIO, output_file: TextIO) -> None:
        """
        Format YAML file and write to output file.
        
        Args:
            input_file (TextIO): Input file object
            output_file (TextIO): Output file object
        """
        yaml_str = input_file.read()
        formatted = self.format_yaml(yaml_str)
        output_file.write(formatted)

# Global printer instance for convenience
_yaml_printer = None

def configure_printer(indent: int = 2, width: int = 80, allow_unicode: bool = True,
                     explicit_start: bool = False, explicit_end: bool = False,
                     sort_keys: bool = False, default_style: Optional[str] = None,
                     default_flow_style: bool = False, line_break: Optional[str] = None,
                     encoding: Optional[str] = None, canonical: bool = False,
                     version: Optional[tuple] = None, tags: Optional[dict] = None) -> None:
    """Configure the global YAML printer instance with given settings.
    
    Args:
        indent (int): Number of spaces for indentation
        width (int): Maximum line width
        allow_unicode (bool): Allow unicode characters
        explicit_start (bool): Include document start marker
        explicit_end (bool): Include document end marker
        sort_keys (bool): Sort dictionary keys
        default_style (str): Default scalar style
        default_flow_style (bool): Use flow style for collections
        line_break (str): Line break style
        encoding (str): Output encoding
        canonical (bool): Use canonical YAML form
        version (tuple): YAML version tuple
        tags (dict): Custom tag definitions
    """
    global _yaml_printer
    _yaml_printer = Yaypp(indent=indent, width=width, allow_unicode=allow_unicode,
                         explicit_start=explicit_start, explicit_end=explicit_end,
                         sort_keys=sort_keys, default_style=default_style,
                         default_flow_style=default_flow_style, line_break=line_break,
                         encoding=encoding, canonical=canonical, version=version,
                         tags=tags)
    return _yaml_printer

def get_printer() -> Yaypp:
    """Get the global YAML printer instance."""
    if not _yaml_printer:
        configure_printer()
    return _yaml_printer

def format_yaml(yaml_str: str) -> str:
    """
    Format YAML string using global printer instance.
    
    Args:
        yaml_str (str): Input YAML string
        
    Returns:
        str: Formatted YAML string
    """
    return get_printer().format_yaml(yaml_str)

def format_file(input_file: TextIO, output_file: TextIO) -> None:
    """
    Format YAML file using global printer instance.
    
    Args:
        input_file (TextIO): Input file object
        output_file (TextIO): Output file object
    """
    get_printer().format_file(input_file, output_file)
