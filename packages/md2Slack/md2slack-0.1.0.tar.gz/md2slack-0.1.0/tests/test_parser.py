import pytest
from md2slack import SlackMarkdown

def test_headers():
    parser = SlackMarkdown()
    assert parser("# Heading 1") == "*Heading 1*"
    assert parser("## Heading 2") == "*Heading 2*"


def test_bold_italic():
    parser = SlackMarkdown()
    assert parser("**Bold**") == "*Bold*"
    assert parser("*Italic*") == "_Italic_"
    assert parser("***Bold Italic***") == "*_Bold Italic_*"

def test_strikethrough():
    parser = SlackMarkdown()
    assert parser("~Strikethrough~") == "~Strikethrough~"

def test_inline_code():
    parser = SlackMarkdown()
    assert parser("`Inline Code`") == "`Inline Code`"
def test_code_block():
    parser = SlackMarkdown()
    markdown = """```
def hello():
    print("Hello, Slack!")
```"""
    expected_output = """```
def hello():
    print("Hello, Slack!")
```"""  # Remove extra newline

    assert parser(markdown) == expected_output

def test_lists():
    parser = SlackMarkdown()
    assert parser("- Item 1\n- Item 2") == "- Item 1\n- Item 2"
    assert parser("1. First\n2. Second") == "1. First\n2. Second"

def test_blockquote():
    parser = SlackMarkdown()
    assert parser("> Blockquote") == "> Blockquote"

def test_table():
    parser = SlackMarkdown()
    markdown = """
| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
"""
    expected_output = """```
Column 1   | Column 2  
---------- | ----------
Data 1     | Data 2    
```"""
    assert parser(markdown) == expected_output

def test_mentions():
    parser = SlackMarkdown()
    assert parser("@user") == "<@user>"
    assert parser("#channel") == "<#channel>"

def test_links():
    parser = SlackMarkdown()
    assert parser("[Slack](https://slack.com)") == "<https://slack.com|Slack>"

def test_images():
    parser = SlackMarkdown()
    assert parser("![Alt text](https://image.url)") == "<https://image.url|Alt text>"
