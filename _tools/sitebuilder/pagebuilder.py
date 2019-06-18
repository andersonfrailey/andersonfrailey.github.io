import json
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension, FencedBlockPreprocessor
from jinja2 import Template
from bs4 import BeautifulSoup
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent
TEMPLATE_PATH = Path(CUR_PATH, "templates")
CONTENT_PATH = Path(CUR_PATH, "..", "..", "_mdcontent")
BLOG_PATH = Path(CUR_PATH, "..", "..", "blog")
HOME_PATH = Path(CUR_PATH, "..", "..")


class PageBuilder():
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
        self.required_attributes = {"author", "template", "written",
                                    "last_modified", "cdn", "md_file"}

    def build_site(self):
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
            md = markdown.Markdown()
            fenced_extension = FencedCodeExtension()
            fenced_extension.extendMarkdown(md)
            code_hilite = CodeHiliteExtension(css_class=".highlight")
            code_hilite.extendMarkdown(md)
            content = md.convert(md_text)
            # md_extentions = [
            #     CodeHiliteExtension(),
            #     FencedCodeExtension()
            # ]
            # content = markdown.markdown(md_text, extentions=md_extentions)

            # write page
            post_attrs = {
                "title": post,
                "author": attrs["author"],
                "written": attrs["written"],
                "cdns": attrs["cdn"],
                "last_modified": attrs["last_modified"],
                "content": content
            }
            self.write_page(pathout, template_path, **post_attrs)

            # add page to blog index
            soup = BeautifulSoup(content, "lxml")
            first_graph = soup.find("p")
            heading = str(soup.find("h1")).replace("h1", "h3")
            first_graphs.append({"heading": heading, "graph": first_graph,
                                 "link": web_page})

        # create blog index
        blog_index_pathout = Path(BLOG_PATH, "index.html")
        blog_index_template = Path(TEMPLATE_PATH, "blog_index_template.html")
        self.write_page(blog_index_pathout, blog_index_template,
                        posts=first_graphs)

        # create home page
        # only use three most recent posts for home index
        recent_posts = first_graphs[: self.num_recent]
        home_index_pathout = Path(HOME_PATH, "index.html")
        home_index_template = Path(TEMPLATE_PATH, "index_template.html")
        self.write_page(home_index_pathout, home_index_template,
                        posts=recent_posts)

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
        self.write_page(speaking_pathout, speaking_template,
                        content=speaking_content)

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
    pages = json.loads(Path(CUR_PATH, "posts.json").open("r").read())
    builder = PageBuilder(pages)
    builder.build_site()