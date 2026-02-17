# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'Land Ownership'
copyright = 'Cristopher Erazo, 2026'
author = 'Cristopher Erazo'
release = '0.0.1'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

# autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Napoleon settings (for Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_private_members = False
napoleon_include_special_members = False



html_theme = 'shibuya'  
html_theme_options = {
    'logo_only': False,
}

# HTML static path (only include if directory exists)
if os.path.isdir('_static'):
    html_static_path = ['_static']
else:
    html_static_path = []

# Templates path
if os.path.isdir('_templates'):
    templates_path = ['_templates']
else:
    templates_path = []

# Source suffix
source_suffix = '.rst'

# Master doc
master_doc = 'index'

# Language configuration
language = 'en'

# Sphinx settings
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Pygments options
pygments_style = 'sphinx'


# --------------------------------------------------

# Logo & favicon
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"

# HTML title
html_title = "Land-Ownership Documentation"


# -- Shibuya Theme Options ---------------------------------------------------

html_theme_options = {

    # Repository link (top-right corner)
    "github_url": "https://github.com/CristopherErazo/Land-Ownership",

    # Layout options
    # "page_layout": "default", 
    "page_layout": "compact",

    # Color scheme (you can customize these colors in your custom CSS)
    "accent_color": "green",
    # Optional announcement banner
    # "announcement": "🚀 New version released!",

}

# -- Custom CSS --------------------------------------------------------------

html_css_files = [
    "custom.css",
]