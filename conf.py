# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.append(str(Path('_ext').resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'elasticsearch-tutorial'
copyright = '2026, Miguel Grinberg'
author = 'Miguel Grinberg'
version = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx_design',
    'sphinx_copybutton',
    'sphinxcontrib.mermaid',
    'lang',
]
myst_enable_extensions = ['colon_fence', 'smartquotes', 'replacements', 'deflist']
myst_heading_anchors = 3

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = 'Elasticsearch Tutorial'
html_static_path = ['_static']
html_js_files = ['ext_lang.js']
html_css_files = ['ext_lang.css']
