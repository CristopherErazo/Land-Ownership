# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath('../../src'))

# Project information
project = 'Land Ownership'
copyright = '2026, Cristopher Erazo'
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

# HTML theme
html_theme = 'sphinx_rtd_theme'
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
