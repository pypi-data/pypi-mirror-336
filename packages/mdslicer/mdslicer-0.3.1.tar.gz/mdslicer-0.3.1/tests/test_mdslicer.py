from __future__ import annotations

from textwrap import dedent

from faker import Faker

import pytest

from mdslicer import mdslicer


fake = Faker()
Faker.seed(4321)

title = fake.sentence(nb_words=3)[:-1]
nested = {
    "key1": fake.sentence(nb_words=3)[:-1],
    "key2": fake.sentence(nb_words=3)[:-1],
    "key3": fake.sentence(nb_words=3)[:-1],
}

md_file_header = f"""\
---
title: {title}
nested:
    key1: {nested["key1"]}
    key2: {nested["key2"]}
    key3: {nested["key3"]}
---
"""

expected_header = {
    "title": title,
    "nested": {
        "key1": nested["key1"],
        "key2": nested["key2"],
        "key3": nested["key3"],
    },
}

address = fake.address()

formatted_address = "".join(f"> {line}\n" for line in address.split("\n"))

md_file_content = f"""\
{fake.text()}

It's address is:

{formatted_address}

## {fake.sentence(nb_words=6)[:-1]}

You may want to see [a Map](https://strasmap.eu/Home).

## {fake.sentence(nb_words=5)[:-1]}

### {fake.sentence(nb_words=3)[:-1]}

- {fake.sentence(nb_words=6)[:-1]},
- {fake.sentence(nb_words=2)[:-1]},
- {fake.sentence(nb_words=6)}\
"""


def test_split_header_and_content():
    header, content = mdslicer.split_header_and_content(
        md_file_header + md_file_content
    )
    assert header == expected_header
    assert content == md_file_content


@pytest.fixture
def md_file(tmp_path):
    md_file = tmp_path / "test.md"
    md_file.write_text(md_file_header + md_file_content)
    return md_file


@pytest.fixture
def slicer():
    return mdslicer.MDSlicer()


def additional_parser(md_content: str) -> str:
    return md_content.replace("__to_replace__", "a replacement")


def test_slicer():
    def get_extensions_names(slicer: mdslicer.MDSlicer) -> list[str]:
        """Return the names of the registered extensions"""
        return [ext.__class__.__name__ for ext in slicer.md.registeredExtensions]

    slicer = mdslicer.MDSlicer()
    assert get_extensions_names(slicer) == []

    slicer = mdslicer.MDSlicer(extensions=["attr_list", "fenced_code"])
    extension_names = get_extensions_names(slicer)
    assert "AttrListExtension" in extension_names
    assert "FencedCodeExtension" in extension_names

    slicer = mdslicer.MDSlicer(additional_parser=additional_parser)
    assert slicer.additional_parser("__to_replace__") == "a replacement"


def test_get_sections(slicer):
    html = "<h2>Section 1</h2><p>Content 1</p><h2>Section 2</h2><p>Content 2</p>"
    sections = slicer.get_sections(html)
    assert len(sections) == 2
    assert sections[0]["title"] == "Section 1"
    assert sections[0]["id"] == "section-1"
    assert sections[0]["content"] == "<p>Content 1</p>"
    assert sections[1]["title"] == "Section 2"
    assert sections[1]["id"] == "section-2"
    assert sections[1]["content"] == "<p>Content 2</p>"


def test_slice_md_content(slicer):
    sections = slicer.slice_md_content(md_file_content)

    assert len(sections) == 3
    assert sections[0]["title"] == ""
    assert sections[0]["title"] == ""
    assert sections[0]["id"] == ""
    assert sections[0]["content"] == dedent("""\
        <p>Front politics summer little fast then go. Blue single either crime gas rather.
        Radio rate you reflect suffer federal. Win benefit before yourself phone analysis dark.</p>
        <p>It's address is:</p>
        <blockquote>
        <p>6727 Daniel Drives
        Youngview, OR 82523</p>
        </blockquote>
        """)
    assert sections[1]["title"] == "Base structure science themselves"
    assert sections[1]["id"] == "base-structure-science-themselves"
    assert sections[1]["content"] == dedent("""
        <p>You may want to see <a href="https://strasmap.eu/Home">a Map</a>.</p>
        """)
    assert sections[2]["title"] == "Instead suddenly some night color"
    assert sections[2]["id"] == "instead-suddenly-some-night-color"
    assert sections[2]["content"] == dedent("""
        <h3>Example vote</h3>
        <ul>
        <li>Movement not help today forget,</li>
        <li>Cup,</li>
        <li>Yeah model outside worry factor wrong.</li>
        </ul>""")


def test_parse_md_content_with_additional_parser():
    slicer = mdslicer.MDSlicer(additional_parser=additional_parser)

    md_file_content = dedent(f"""\
        {fake.text()}
        __to_replace__
        It's address is:""")

    sections = slicer.slice_md_content(md_file_content)
    assert len(sections) == 1
    assert "a replacement" in sections[0]["content"]


def test_slice_file(slicer, md_file):
    header, sections = slicer.slice_file(md_file)
    assert header == expected_header
    assert len(sections) == 3


def test_slice_content(slicer):
    header, sections = slicer.slice_content(md_file_header + md_file_content)
    assert header == expected_header
    assert len(sections) == 3
