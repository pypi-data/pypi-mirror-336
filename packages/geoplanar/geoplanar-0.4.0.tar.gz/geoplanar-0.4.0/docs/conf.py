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
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.abspath("../"))


# -- Project information -----------------------------------------------------
import geoplanar

project = "geoplanar"
copyright = "2021-, Serge Rey & geoplanar contributors"
author = "Serge Rey & geoplanar contributors"

# The full version, including alpha/beta/rc tags
release = geoplanar.__version__
version = geoplanar.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc", "numpydoc", "nbsphinx"]

# nbsphinx do not use requirejs (breaks bootstrap)
nbsphinx_requirejs_path = ""

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
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

html_sidebars = {
    "**": ["docs-sidebar.html"],
}

# ---------------------------------------------------------------------------

# Copy notebooks into the docs/ directory so sphinx sees them

HERE = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


files_to_copy = [
    "notebooks/overlaps.ipynb",
    "notebooks/gaps.ipynb",
    "notebooks/holes.ipynb",
    "notebooks/nonplanaredges.ipynb",
    "notebooks/nonplanartouches.ipynb",
    "notebooks/usmex.ipynb",
]


for filename in files_to_copy:
    shutil.copy(HERE / ".." / filename, HERE)


# convert README to rst

subprocess.check_output(["pandoc", "--to", "rst", "-o", "README.rst", "../README.md"])
