import argparse
import json
import requests
import markdown
import pandas as pd
import statstables as st
from datetime import datetime
from jinja2 import Template
from bs4 import BeautifulSoup
from pathlib import Path
from utils import replace_code_blocks, MLB_PROJECTION_COLUMNS, NAME_TO_ABBR
from pybaseball import standings


CUR_PATH = Path(__file__).resolve().parent
TEMPLATE_PATH = Path(CUR_PATH, "templates")
CONTENT_PATH = Path(CUR_PATH, "..", "..", "_mdcontent")
BLOG_PATH = Path(CUR_PATH, "..", "..", "blog")
HOME_PATH = Path(CUR_PATH, "..", "..")
DATA_PATH = Path(CUR_PATH, "..", "..", "code", "data")
YEAR = 2025
OPENING_DAY = "03272025"
FINAL_DAY = "09282025"
SATCHEL_URL = f"https://raw.githubusercontent.com/andersonfrailey/satchel/refs/heads/main/projections/satchel{YEAR}.csv"
PERCENTILES_URL = f"https://raw.githubusercontent.com/andersonfrailey/satchel/refs/heads/main/projections/percentiles{YEAR}.json"


class PageBuilder:
    """
    Receives a path to a JSON file containing metadata for a list of web pages
    to be built. The metadata contains information on where the final HTML
    file should be saved, which HTML template to use, and where the markdown
    content for that page can be found.
    Page metadata schema:
    {
        'Page Title': {
            'template': either a path to the HTML template or null. If null,
                        defaults to '../templates/page_template.html',
            'content': path to a markdown file with the content to be rendered
                       to HTML,
            'pathout': path to where the final file should be saved
        }
    }
    """

    def __init__(self, pages: dict, num_recent: int = 3):
        """
        This class is used to create generic web pages for PSL
        Parameters
        ----------
        pages: dictionary containing information on all the pages to be created
        num_recent: number of posts to display on home page
        Returns
        -------
        None
        """
        self.pages = pages
        self.num_recent = num_recent
        self.required_attributes = {
            "author",
            "template",
            "written",
            "last_modified",
            "cdn",
            "md_file",
        }

    def build_site(self, season_summary=False, skip_projections=False):
        """
        Function for building the blog portion of the site
        """
        # hold first paragraph of each post
        first_graphs = []
        # loop through each post and create the template
        for post, attrs in self.pages.items():
            assert self.required_attributes.issubset(set(attrs.keys()))
            web_page = "-".join(post.split()) + ".html"
            pathout = Path(BLOG_PATH, web_page)
            template_path = Path(TEMPLATE_PATH, attrs["template"])
            md_text = Path(CONTENT_PATH, attrs["md_file"]).open("r").read()
            _md_text = replace_code_blocks(md_text)
            md = markdown.Markdown()
            content = md.convert(_md_text)

            # write page
            post_attrs = {
                "title": post,
                "author": attrs["author"],
                "written": attrs["written"],
                "cdns": attrs["cdn"],
                "last_modified": attrs["last_modified"],
                "content": content,
            }
            self.write_page(pathout, template_path, **post_attrs)

            # add page to blog index
            soup = BeautifulSoup(content, "lxml")
            first_graph = soup.find("p")
            heading = str(soup.find("h1")).replace("h1", "h3")
            first_graphs.append(
                {"heading": heading, "graph": first_graph, "link": web_page}
            )

        # create blog index page
        blog_index_pathout = Path(BLOG_PATH, "index.html")
        blog_index_template = Path(TEMPLATE_PATH, "blog_index_template.html")
        self.write_page(blog_index_pathout, blog_index_template, posts=first_graphs)

        # create home page
        # only use three most recent posts for home index
        index_md_text = Path(CONTENT_PATH, "index.md").open("r").read()
        index_content = markdown.markdown(index_md_text)
        jmp_md_text = Path(CONTENT_PATH, "jmp_content.md").open("r").read()
        jmp_content = markdown.markdown(jmp_md_text)
        recent_posts = first_graphs[: self.num_recent]
        home_index_pathout = Path(HOME_PATH, "index.html")
        home_index_template = Path(TEMPLATE_PATH, "index_template.html")
        self.write_page(
            home_index_pathout,
            home_index_template,
            content=index_content,
            posts=recent_posts,
            jmp_content=jmp_content,
        )

        # create about page
        about_md_text = Path(CONTENT_PATH, "about.md").open("r").read()
        about_content = markdown.markdown(about_md_text)
        about_template = Path(TEMPLATE_PATH, "about_template.html")
        about_pathout = Path(HOME_PATH, "about.html")
        self.write_page(about_pathout, about_template, content=about_content)

        # create speaking page
        speaking_md_text = Path(CONTENT_PATH, "speaking.md").open("r").read()
        speaking_content = markdown.markdown(speaking_md_text)
        speaking_template = Path(TEMPLATE_PATH, "speaking_template.html")
        speaking_pathout = Path(HOME_PATH, "speaking.html")
        self.write_page(speaking_pathout, speaking_template, content=speaking_content)

        # create research page
        research_md_text = Path(CONTENT_PATH, "research.md").open("r").read()
        research_content = markdown.markdown(research_md_text)
        research_template = Path(TEMPLATE_PATH, "research_template.html")
        research_pathout = Path(HOME_PATH, "research.html")
        self.write_page(research_pathout, research_template, content=research_content)

        # create MLB projections page
        if not skip_projections:
            mlb_projections_text = (
                Path(CONTENT_PATH, "mlb-projections.md").open("r").read()
            )
            mlb_projections_content = markdown.markdown(mlb_projections_text)
            # fetch projections
            mlb_projections = pd.read_csv(
                SATCHEL_URL, index_col=None, parse_dates=["date"]
            )
            r = requests.get(PERCENTILES_URL)
            results = json.loads(r.text)
            if season_summary:
                mlb_projections["date"] = mlb_projections["date"].apply(
                    lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0)
                )
                opening_day = mlb_projections[
                    mlb_projections["date"] == datetime.strptime(OPENING_DAY, "%m%d%Y")
                ]
                final_standings = pd.concat(standings(YEAR))
                final_standings["Team"] = final_standings["Tm"].map(NAME_TO_ABBR)
                final_standings["W"] = final_standings["W"].astype(int)
                final_standings["L"] = final_standings["L"].astype(int)
                proj_columns = [
                    "Team",
                    "Projected Wins",
                    "Projected Losses",
                    "Make Playoffs (%)",
                    "Make Wild Card (%)",
                    "Win Division (%)",
                    "Win League (%)",
                    "Win WS (%)",
                ]
                comparison_data = pd.merge(
                    opening_day[proj_columns],
                    final_standings[["Team", "W", "L", "W-L%"]],
                    on="Team",
                )
                comparison_data["Season Percentile"] = comparison_data.apply(
                    lambda x: round(results[x["Team"]][str(int(x["W"]))] * 100, 2),
                    axis=1,
                )
                comparison_data["Projected - Actual Wins"] = (
                    comparison_data["Projected Wins"] - comparison_data["W"]
                )
                comparison_data.sort_values("W", inplace=True, ascending=False)
                comparison_table = st.tables.GenericTable(comparison_data)
                comparison_table.sig_digits = 2
                comparison_table.include_index = False
                comparison_table.rename_columns(
                    {"Projected Wins": "W", "Projected Losses": "L"}
                )
                comparison_table.add_multicolumns(
                    columns=["", "Projected Outcomes", "Actual", ""],
                    spans=[1, 7, 3, 2],
                    underline=False,
                )
                mlb_projections_table_html = comparison_table.render_html(
                    table_class="dataframe"
                )
                max_diff = comparison_data["Projected - Actual Wins"].abs().max()
                max_diff_team = comparison_data["Team"][
                    comparison_data["Projected - Actual Wins"] == max_diff
                ].values
                max_diff_team = ", ".join(max_diff_team)
                min_diff = comparison_data["Projected - Actual Wins"].abs().min()
                min_diff_team = comparison_data["Team"][
                    comparison_data["Projected - Actual Wins"] == min_diff
                ].values
                min_diff_team = ", ".join(min_diff_team)
                avg_diff = comparison_data["Projected - Actual Wins"].abs().mean()
                avg_diff_all = comparison_data["Projected - Actual Wins"].mean()
                max_over = comparison_data["Projected - Actual Wins"].max()
                max_over_team = comparison_data["Team"][
                    comparison_data["Projected - Actual Wins"] == max_over
                ].values
                max_over_team = ", ".join(max_over_team)
                max_under = comparison_data["Projected - Actual Wins"].min()
                max_under_team = comparison_data["Team"][
                    comparison_data["Projected - Actual Wins"] == max_under
                ].values
                max_under_team = ", ".join(max_under_team)
                summary_stats = (
                    f"Average difference between projected and actual wins: {avg_diff_all:.2f} wins<br>"
                    f"Average difference between projected and actual wins (absolute value): {avg_diff:.2f} wins<br>"
                    f"Largest over projection: {max_over} wins ({max_over_team})<br>"
                    f"Largest under projection: {max_under} wins ({max_under_team})<br>"
                    f"Maximum difference between projected and actual wins (absolute value): {max_diff} wins ({max_diff_team})<br>"
                    f"Minimum difference between projected and actual wins (absolute value): {min_diff} wins ({min_diff_team})<br>"
                )
                last_modified_date = datetime.today().strftime("%B %d, %Y")
                css = "projections_css2.css"
            else:
                # only use the most recent projections
                max_date = mlb_projections["date"].max()
                mlb_projections = mlb_projections[mlb_projections["date"] == max_date]
                mlb_projections["Projected Wins"] = mlb_projections[
                    "Projected Wins"
                ].astype(int)
                mlb_projections.drop("date", axis=1, inplace=True)
                mlb_projections.sort_values(
                    "Projected Wins", ascending=False, inplace=True
                )
                mlb_projections["Season Percentile"] = mlb_projections.apply(
                    lambda x: round(
                        results[x["Team"]][str(x["Projected Wins"])] * 100, 2
                    ),
                    axis=1,
                )
                # order and filter columns
                mlb_projections = mlb_projections[
                    [
                        "Team",
                        "Wins to Date",
                        "Losses to Date",
                        "Wins RoS",
                        "Losses RoS",
                        "Projected Wins",
                        "Projected Losses",
                        "Make Wild Card (%)",
                        "Win Division (%)",
                        "Make Playoffs (%)",
                        "Win League (%)",
                        "Win WS (%)",
                        "Season Percentile",
                    ]
                ]
                col_labels = {
                    "Wins to Date": "W",
                    "Losses to Date": "L",
                    "Wins RoS": "W",
                    "Losses RoS": "L",
                    "Projected Wins": "W",
                    "Projected Losses": "L",
                }
                mlb_projections_table = st.tables.GenericTable(
                    mlb_projections,
                    include_index=False,
                    column_labels=col_labels,
                    sig_digits=2,
                    formatters={col: lambda x: f"{x:.0f}" for col in col_labels.keys()},
                )
                mlb_projections_table.add_multicolumns(
                    ["", "To Date", "RoS", "Projections"],
                    spans=[1, 2, 2, 8],
                    underline=False,
                )
                mlb_projections_table_html = mlb_projections_table.render_html(
                    table_class="dataframe"
                )
                last_modified_date = max_date.strftime("%B %d, %Y")
                css = "projections_css.css"
                summary_stats = ""
            mlb_projections_template = Path(
                TEMPLATE_PATH, "mlb_projections_template.html"
            )
            mlb_projections_pathout = Path(HOME_PATH, "mlb-projections.html")

            self.write_page(
                mlb_projections_pathout,
                mlb_projections_template,
                content=mlb_projections_content,
                projections=mlb_projections_table_html,
                last_modified=last_modified_date,
                css=css,
                summary_stats=summary_stats,
            )

    def write_page(self, pathout, template_path, **kwargs):
        """
        Render the HTML template with the markdown text
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--season-summary",
        action="store_true",
        help="Make the MLB Projections table a comparison of the open day projections to end of season results.",
    )
    parser.add_argument(
        "--skip-projections",
        action="store_true",
        help="If included, MLB projections are skipped",
    )
    args = parser.parse_args()
    pages = json.loads(Path(CUR_PATH, "posts.json").open("r").read())
    builder = PageBuilder(pages)
    builder.build_site(
        season_summary=args.season_summary, skip_projections=args.skip_projections
    )
