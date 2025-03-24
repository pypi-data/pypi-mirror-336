"""A library to slice a markdown file into HTML sections."""

__version__ = "0.3.1"

from .mdslicer import MDSlicer, split_header_and_content

__all__ = ["MDSlicer", "split_header_and_content"]
