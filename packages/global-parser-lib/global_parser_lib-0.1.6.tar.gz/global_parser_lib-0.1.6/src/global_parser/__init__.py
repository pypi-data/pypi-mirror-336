"""
global_parser_lib - A library for parsing various file types.

This library provides parsers for different file types including images and audio files.
"""

__version__ = "0.1.0"

# Import main components to make them available at the package level
from global_parser.core import FileParser, UrlParser

__all__ = ["FileParser","UrlParser"] 