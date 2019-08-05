from jinja2 import Template
from pathlib import Path
from bs4 import BeautifulSoup
# this should embed the path to the file(?) inside script tags using vegaembed
# could save as HTML file, read that file, pull the div with the code in it,
# then delete the file


def altair_fix(html: str, i: int):
    """
    Replaces certain keywords in the JavaScript needed to show altair plots.
    Allows multiple altair plots to be rendered with vega on a single page
    """
    # convert beautiful soup tag to a string
    html = str(html)
    keywords = ["vis", "spec", "embed_opt", "const el"]
    for word in keywords:
        html = html.replace(word, f"{word}{str(i)}")
    return f'<div id="vis{i}"></div>\n' + html


def write_page(pathout, template_path, **kwargs):
    """
    Render the MD template with the HTML for the plots inserted
    Parameters
    ----------
    pathout: path where the HTML file will be saved
    template_path: path for the HTML template
    Returns
    -------
    None
    """
    # read and render HTML template
    template_str = Path(template_path).open("r").read()
    template = Template(template_str)
    rendered = template.render(**kwargs)
    Path(pathout).write_text(rendered)


def add_plots(pathout, template_path, plots: dict, altair=False):
    """
    """
    plots_content = {}
    for i, name in enumerate(plots):
        html = plots[name]
        content = open(html, "r").read()
        soup = BeautifulSoup(content, "lxml")
        body = soup.find("body")
        script = body.find("script")
        if altair:
            script = altair_fix(script, i + 1)
        plots_content[name] = script
    write_page(pathout, template_path, **plots_content)
