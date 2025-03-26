# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib.metadata

project = "AESOpt param"
author = "Kenneth Lønbæk"
release = importlib.metadata.version("aesoptparam")

root_doc = "main"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_design",
    "sphinx_external_toc",
    "sphinxcontrib.bibtex",
    "myst_nb",
    "sphinx.ext.autodoc",
]
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
    "html_image",
    "dollarmath",
]
exclude_patterns = []
sd_fontawesome_latex = True

html_theme = "sphinx_book_theme"

html_context = {"default_mode": "dark"}
html_show_sourcelink = False
html_theme_options = {
    "path_to_docs": "docs",
    "home_page_in_toc": False,
}
html_title = project

external_toc_path = "_toc.yml"  # optional, default: _toc.yml
external_toc_exclude_missing = False  # optional, default: False
bibtex_bibfiles = ["references.bib"]
nb_custom_formats = {".py": ["jupytext.reads", {"fmt": "py"}]}
nb_execution_timeout = -1
