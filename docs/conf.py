# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "rlapi"
copyright = "2018-2020, Jakub Kuczys (jack1142)"
author = "Jakub Kuczys (jack1142)"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# pylint: disable=wrong-import-position
from rlapi import __version__  # noqa: E402

# The short X.Y version.
version = __version__

# The full version, including alpha/beta/rc tags.
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxcontrib_trio",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Role which is assigned when you make a simple reference within backticks
default_role = "any"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Use old HTML4 writer because sphinx_rtd_theme doesn't support new one yet
html4_writer = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for linkcheck builder ----------------------------------------

# A list of regular expressions that match URIs that should not be
# checked when doing a linkcheck build.
linkcheck_ignore = [r"https://rltracker.pro*"]
linkcheck_retries = 3


# -- Options for extensions -----------------------------------------------

# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}

# autodoc
autodoc_member_order = "bysource"
autodoc_typehints = "none"


def setup(app):
    app.add_stylesheet("style.css")
