import packaging.version
import sphinx_bootstrap_theme
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# Project --------------------------------------------------------------

project = "flask_covid19"
copyright = "2020 Thomas Wöhlke"
author = "thomaswoehlke"
release, version = get_version("flask_covid19")

# General --------------------------------------------------------------

master_doc = "index"

extensions = [
    "myst_parser"  # ,
    # "sphinx.ext.autodoc",
    # "sphinx.ext.intersphinx",
    # "sphinx_bootstrap_theme",
    # "sphinxcontrib.log_cabinet",
    # "sphinxcontrib.gravizo",
    # "sphinxcontrib.srclinks",
    # "pallets_sphinx_themes",
    # "sphinx_issues",
    # "sphinx_tabs.tabs",
]
source_suffix = {
    #'.rst': 'restructuredtext',
    ".txt": "markdown",
    ".md": "markdown",
}
autodoc_typehints = "description"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
    "click": ("https://click.palletsprojects.com/", None),
    "jinja": ("https://jinja.palletsprojects.com/", None),
    "itsdangerous": ("https://itsdangerous.palletsprojects.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/", None),
    "wtforms": ("https://wtforms.readthedocs.io/", None),
    "blinker": ("https://pythonhosted.org/blinker/", None),
}
issues_github_path = "thomaswoehlke/flask_covid19"

# HTML -----------------------------------------------------------------

html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("Donate", "https://www.paypal.com/paypalme/ThomasWoehlke"),
        ProjectLink("PyPI Releases", "https://pypi.org/project/flask_covid19/"),
        ProjectLink("Source Code", "https://github.com/thomaswoehlke/flask_covid19/"),
        ProjectLink(
            "Issue Tracker", "https://github.com/thomaswoehlke/flask_covid19/issues/"
        ),
        ProjectLink("Website", "https://woehlke.org/p/flask_covid19/"),
        ProjectLink("Twitter", "https://twitter.com/SearchSquirrel"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]
html_favicon = "_static/flask-icon.png"
html_logo = "_static/flask-icon.png"
html_title = f"flask_covid19 Documentation ({version})"
# html_title = f"flask_covid19 Documentation"
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [(master_doc, f"Flask.tex", html_title, author, "manual")]

# Local Extensions -----------------------------------------------------


def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    app = inliner.document.settings.env.app
    release = app.config.release
    base_url = "https://github.com/thomaswoehlke/flask_covid19/tree/"

    if text.endswith(">"):
        words, text = text[:-1].rsplit("<", 1)
        words = words.strip()
    else:
        words = None

    if packaging.version.parse(release).is_devrelease:
        url = f"{base_url}main/{text}"
    else:
        url = f"{base_url}{release}/{text}"

    if words is None:
        words = url

    from docutils.nodes import reference
    from docutils.parsers.rst.roles import set_classes

    options = options or {}
    set_classes(options)
    node = reference(rawtext, words, refuri=url, **options)
    return [node], []


def setup(app):
    app.add_role("gh", github_link)
