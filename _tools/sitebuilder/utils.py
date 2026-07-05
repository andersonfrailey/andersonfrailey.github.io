"""
Helper functions for the page builder utility
"""

import json
import re
from datetime import datetime
from pathlib import Path


# order sections should appear in on the research page, and the heading to
# use for each paper "type" found in papers.json
PAPER_SECTIONS = [
    ("working_paper", "Working Papers"),
    ("published", "Published Papers"),
    ("other", "Other Publications"),
]


def _slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def _format_paper_date(date_str):
    """
    Converts a "YYYY-MM-DD" date string into "Month D, YYYY" (e.g. "May 30, 2017")
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def _render_paper(title, attrs, section_type):
    """
    Renders a single paper's metadata (from papers.json) as an HTML block.
    Dates are only shown for published/other work, not working papers.
    """
    link = attrs.get("link", "")
    if link:
        title_html = f'<a href="{link}"><strong><em>{title}</em></strong></a>'
    else:
        title_html = f"<strong><em>{title}</em></strong>"

    lines = [f'<p class="paper-title">{title_html}</p>']

    coauthors = attrs.get("coauthors", "")
    if coauthors:
        lines.append(f'<p class="paper-coauthors">with {coauthors}</p>')

    outlet = attrs.get("outlet", "")
    if section_type == "working_paper":
        meta = outlet
    else:
        date_str = _format_paper_date(attrs["date"])
        meta = f"{outlet}, {date_str}" if outlet else date_str
    if meta:
        lines.append(f'<p class="paper-meta"><em>{meta}</em></p>')

    abstract = attrs.get("abstract", "")
    if abstract:
        anchor = f"abstract-{_slugify(title)}"
        lines.append(
            '<p class="paper-abstract-toggle">'
            f'<a href="#" class="abstract-toggle" data-target="{anchor}">'
            '<span class="abstract-arrow">&#9654;</span> Abstract'
            "</a></p>"
        )
        lines.append(f'<p class="paper-abstract" id="{anchor}" hidden>{abstract}</p>')

    return "<div class=\"paper\">\n" + "\n".join(lines) + "\n</div>"


def build_papers_html(papers_path):
    """
    Reads papers.json and builds the HTML for the Working Papers, Published
    Papers, and Other Publications sections of the research page. Papers are
    grouped by their "type" field and, within each group, ordered newest to
    oldest by date. Sections with no papers are omitted.
    """
    papers = json.loads(Path(papers_path).read_text())

    grouped = {section_type: [] for section_type, _ in PAPER_SECTIONS}
    for title, attrs in papers.items():
        grouped.setdefault(attrs["type"], []).append((title, attrs))

    html_parts = []
    for section_type, heading in PAPER_SECTIONS:
        section_papers = grouped.get(section_type, [])
        if not section_papers:
            continue
        section_papers.sort(key=lambda p: p[1]["date"], reverse=True)
        html_parts.append(f"<h2>{heading}</h2>")
        html_parts.extend(
            _render_paper(title, attrs, section_type) for title, attrs in section_papers
        )

    return "\n".join(html_parts)


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
