"""
Helper functions for the page builder utility
"""

import re
from pathlib import Path


def replace_math_blocks(text):
    """
    Wraps $$...$$ (display) and $...$ (inline) in raw HTML so the markdown
    converter doesn't mangle LaTeX content (underscores, asterisks, etc.).
    Converts to MathJax's default delimiters: \[...\] and \(...\).
    Display math must be matched first to avoid double-matching.
    """
    text = re.sub(
        r'\$\$(.+?)\$\$',
        lambda m: f'<div>$${m.group(1)}$$</div>',
        text,
        flags=re.DOTALL
    )
    text = re.sub(
        r'\$(.+?)\$',
        lambda m: f'<span>${m.group(1)}$</span>',
        text
    )
    return text


def replace_table_includes(text, base_path):
    """
    Replaces {{table: path/to/table.html}} placeholders with the contents
    of the referenced HTML file. Paths are relative to base_path (repo root).
    """
    pattern = r"(?:<p>)?\{\{table:\s*(.+?)\}\}(?:</p>)?"
    for match in re.finditer(pattern, text):
        filepath = Path(base_path, match.group(1).strip())
        table_html = filepath.read_text()
        text = text.replace(match.group(0), table_html)
    return text


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
    grouped_pattern = r"(```[\w]+\n)([^`]+)(```)"
    # replace code blocks with language specification
    code_blocks = re.findall(grouped_pattern, text)
    end_html = "</code></pre>\n"
    for block in code_blocks:
        lang = block[0].lstrip("```").rstrip()
        start_html = f'<pre><code class="{lang}">'
        new_str = start_html + block[1] + end_html
        old_str = block[0] + block[1] + block[2]
        text = text.replace(old_str, new_str)

    return text


MLB_PROJECTION_COLUMNS = [
    ("", "Team"),
    ("To Date", "W"),
    ("To Date", "L"),
    ("Rest of Season", "W"),
    ("Rest of Season", "L"),
    ("Total", "W"),
    ("Total", "L"),
    ("Total", "Make Playoffs (%)"),
    ("Total", "Make Wild Card (%)"),
    ("Total", "Win Division (%)"),
    ("Total", "Win League (%)"),
    ("Total", "Win World Series (%)"),
    ("Total", "Season Percentile"),
]

ABBR_TO_NAME = {
    "ARI": "Arizona Diamondbacks",
    "ATL": "Atlanta Braves",
    "BAL": "Baltimore Orioles",
    "BOS": "Boston Red Sox",
    "CHC": "Chicago Cubs",
    "CHW": "Chicago White Sox",
    "CIN": "Cincinnati Reds",
    "CLE": "Cleveland Guardians",
    "COL": "Colorado Rockies",
    "DET": "Detroit Tigers",
    "MIA": "Miami Marlins",
    "HOU": "Houston Astros",
    "KCR": "Kansas City Royals",
    "LAD": "Los Angeles Dodgers",
    "MIL": "Milwaukee Brewers",
    "NYM": "New York Mets",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SDP": "San Diego Padres",
    "SFG": "San Francisco Giants",
    "STL": "St. Louis Cardinals",
    "WSN": "Washington Nationals",
    "LAA": "Los Angeles Angels",
    "MIN": "Minnesota Twins",
    "NYY": "New York Yankees",
    "OAK": "Oakland Athletics",
    "SEA": "Seattle Mariners",
    "TBR": "Tampa Bay Rays",
    "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays",
}

NAME_TO_ABBR = {name: abbr for abbr, name in ABBR_TO_NAME.items()}
