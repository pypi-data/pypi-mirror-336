# MDSlicer

[![pipeline status](https://github.com/boileaum/mdslicer/actions/workflows/test.yml/badge.svg)](https://github.com/boileaum/mdslicer/actions)
[![cov](https://boileaum.github.io/mdslicer/coverage.svg)](https://boileaum.github.io/mdslicer/coverage)
[![Latest Release](https://img.shields.io/github/v/release/boileaum/mdslicer?label=release)](https://github.com/boileaum/mdslicer/releases)
[![Doc](https://img.shields.io/badge/doc-sphinx-blue)](https://boileaum.github.io/mdslicer)

A library to slice a markdown file into HTML sections.

## Installation

```bash
pip install mdslicer
```

## Usage

A common usage when converting a markdown file to HTML is to extract a YAML header and split the markdown content into sections delimited by h2 titles.
This library uses:

- the [`frontmatter`](https://pypi.org/project/python-frontmatter/) library to extract metadata from the header,
- the [`markdown`](https://python-markdown.github.io/) library to parse the markdown into html and build a table of contents,
- the [`beautifulsoup`](https://pypi.org/project/beautifulsoup4/) library to split the html into sections

Sections can then be used to generate an HTML file with a table of contents, for example using jinja2 templates:

```python
from mdslicer import MDSlicer
from jinja2 import Template

slicer = MDSlicer(extensions=['fenced_code'])
header, sections = slicer.slice_file("README.md")

template = Template(
"""
<h1>MDSlicer</h1>
<h2>Table of contents</h2>
<ul>
{% for section in sections[1:] %}
    <li><a href="#{{ section.id }}">{{ section.title }}</a></li>
{% endfor %}
</ul>
{% for section in sections %}
<section id="{{ section.id }}">
    <h2>{{ section.title }}</h2>
    {{ section.content }}
</section>
{% endfor %}
"""
)
html = template.render(sections=sections)
print(html)
```
