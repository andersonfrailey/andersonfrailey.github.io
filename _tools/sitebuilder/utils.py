"""
Helper functions for the page builder utility
"""
import re


def replace_code_blocks(text):
    """
    This function searches the provided text for code blocks in standard
    markdown format and replaces them with HTML used by highlightjs
    for code highlighting in HTML.
    If the block starts with ```{language}\n then it will pull the language
    specified and place it in the highlighjs class attribute

    Parameters
    ----------
    text: Markdown text with code blocks
    """
    # pattern used by markdown code blocks
    grouped_pattern = r'(```[\w]+\n)([^`]+)(```)'
    # replace code blocks with language specification
    code_blocks = re.findall(grouped_pattern, text)
    end_html = '</code></pre>\n'
    for block in code_blocks:
        lang = block[0].lstrip('```').rstrip()
        start_html = f'<pre><code class="{lang}">'
        new_str = start_html + block[1] + end_html
        old_str = block[0] + block[1] + block[2]
        text = text.replace(old_str, new_str)

    return text
