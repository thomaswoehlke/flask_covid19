# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))

import packaging.version
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# -- Project information -----------------------------------------------------

project = "flask_covid19"
copyright = "2021, Thomas Woehlke"
author = "Thomas Woehlke"

# The full version, including alpha/beta/rc tags
release = "0.0.78"
version = "0.0.78"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
master_doc = "index"

extensions = [
    "myst_parser",
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
]

source_suffix = {
    ".rst": "restructuredtext",
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

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": True}
html_context = {
    "project_links": [
        ProjectLink("Donate", "https://www.paypal.com/paypalme/ThomasWoehlke"),
        ProjectLink("PyPI Releases", "https://pypi.org/project/Flask_covid19/"),
        ProjectLink("Source Code", "https://github.com/thomaswoehlke/flask_covid19/"),
        ProjectLink(
            "Issue Tracker", "https://github.com/thomaswoehlke/flask_covid19/issues/"
        ),
        ProjectLink("Website", "https://palletsprojects.com/p/flask_covid19/"),
        ProjectLink("Twitter", "https://twitter.com/ThomasWoehlke"),
        ProjectLink("Chat", "https://discord.gg/ThomasWoehlke"),
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
html_title = f"Flask Documentation ({version})"
html_show_sourcelink = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "flask"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# LaTeX ----------------------------------------------------------------

latex_documents = [(master_doc, f"Flask-{version}.tex", html_title, author, "manual")]

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
