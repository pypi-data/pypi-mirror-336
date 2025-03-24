"""
Parse markdown file into header and sections.
A header is a dictionary with the metadata of the markdown file.
Sections are a list of dictionaries with the title, id and content of each section.
For example:

.. highlight:: python
.. code-block:: python

    sections =
    [{'title': 'Section 1', 'id': 'section-1', 'content': '\\n<p>Content 1</p>\\n'},
     {'title': 'Section 2', 'id': 'section-2', 'content': '\\n<p>Content 2</p>'}]

"""

from __future__ import annotations  # for compatibility with Python < 3.10
from pathlib import Path
from typing import Callable

import bs4
import frontmatter
import markdown  # type: ignore
from markdown.extensions.toc import slugify


def split_header_and_content(file_content: str) -> tuple[dict, str]:
    """
    Split a markdown file content into a YAML header and a content

    Args:
        file_content: content of the markdown file

    Returns:
        header of the markdown file,
        content of the markdown file
    """
    header, md_content = frontmatter.parse(file_content)
    return header, md_content


class MDSlicer:
    """
    Parse markdown content into metadata header and sections
    """

    def __init__(self, additional_parser: Callable | None = None, **kwargs):
        """
        Create a markdown parser with the given extensions.


        Args:
            additional_parser: Additional parser to apply on the markdown content
            kwargs: Keyword arguments to pass to the `markdown.Markdown() <https://python-markdown.github.io/reference/#Markdown>`_ parser initializer (such as the list of extensions)
        """
        self.md = markdown.Markdown(**kwargs)
        self.md.reset()
        self.additional_parser = additional_parser

    def slice_md_content(self, md_content: str) -> list[dict[str, str]]:
        """
        Convert markdown content to HTML sections.

        Args:
            md_content: Markdown content

        Returns:
            List of sections

        Example:
            >>> from mdslicer import MDSlicer
            >>> slicer = MDSlicer()
            >>> md_content = '''
            ... # Title
            ...
            ... Some content
            ...
            ... ## Section 1
            ...
            ... Content 1
            ...
            ... ## Section 2
            ...
            ... Content 2'''
            >>> slicer.slice_md_content(md_content)  # doctest: +NORMALIZE_WHITESPACE
            [{'title': '', 'id': '', 'content': '<h1>Title</h1>\\n<p>Some content</p>\\n'},
            {'title': 'Section 1', 'id': 'section-1', 'content': '\\n<p>Content 1</p>\\n'},
            {'title': 'Section 2', 'id': 'section-2', 'content': '\\n<p>Content 2</p>'}]
        """
        if self.additional_parser:
            md_content = self.additional_parser(md_content)
        self.md.reset()
        html = self.md.convert(md_content)
        sections = self.get_sections(html)

        return sections

    def get_sections(self, html: str) -> list[dict[str, str]]:
        """
        Get sections from the HTML content by splitting it with h2 tags

        Args:
            html: HTML content

        Returns:
            List of sections with an id, a title and an html content

        Example:
            >>> from mdslicer import MDSlicer
            >>> slicer = MDSlicer()
            >>> html = "<h2>Section 1</h2><p>Content 1</p><h2>Section 2</h2><p>Content 2</p>"
            >>> slicer.get_sections(html)  # doctest: +NORMALIZE_WHITESPACE
            [{'title': 'Section 1', 'id': 'section-1', 'content': '<p>Content 1</p>'},
             {'title': 'Section 2', 'id': 'section-2', 'content': '<p>Content 2</p>'}]
        """

        # Build section dict
        soup = bs4.BeautifulSoup(html, "html.parser")
        sections = []

        # If section does not start with a h2 tag
        no_h2_section = ""
        for tag in soup:
            if tag.name == "h2":  # type: ignore
                break
            else:
                no_h2_section += str(tag)

        if no_h2_section:
            sections.append({"title": "", "id": "", "content": no_h2_section})

        # Parse the rest
        for h2 in soup.find_all("h2"):
            title = h2.text
            content = ""
            for tag in h2.next_siblings:
                if tag.name == "h2":  # type: ignore
                    break
                content += str(tag)
            section = {"title": title, "id": slugify(title, "-"), "content": content}
            sections.append(section)

        return sections

    def slice_content(self, file_content: str) -> tuple[dict, list[dict[str, str]]]:
        """
        Parse a markdown string into a YAML header and a content

        Args:
            file_content: content of the markdown file

        Returns:
            header of the markdown file,
            content sections of the markdown file

        Examples:
            >>> slicer = MDSlicer()
            >>> file_content = '''
            ... ---
            ... title: Example
            ... ---
            ...
            ... ## Section 1
            ...
            ... Content 1
            ...
            ... ## Section 2
            ...
            ... Content 2'''
            >>> header, sections = slicer.slice_content(file_content)
            >>> print(header)
            {'title': 'Example'}
            >>> sections    # doctest: +NORMALIZE_WHITESPACE
            [{'title': 'Section 1', 'id': 'section-1', 'content': '\\n<p>Content 1</p>\\n'},
             {'title': 'Section 2', 'id': 'section-2', 'content': '\\n<p>Content 2</p>'}]

        """
        header, md_content = split_header_and_content(file_content)
        sections = self.slice_md_content(md_content)
        return header, sections

    def slice_file(self, mdfile_path: str | Path) -> tuple[dict, list[dict[str, str]]]:
        """
        Parse a markdown file into a YAML header and a content

        Args:
            mdfile_path: Path to the markdown file

        Returns:
            header of the markdown file,
            content sections of the markdown file,
        """
        mdfile_path = Path(mdfile_path)
        file_content = mdfile_path.read_text()
        return self.slice_content(file_content)
