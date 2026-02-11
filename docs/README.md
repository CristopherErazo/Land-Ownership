# Documentation

This directory contains the Sphinx documentation source for the Land Ownership project. -

## Building Documentation Locally

### Prerequisites

Ensure you have Sphinx and required extensions installed:

```bash
pip install sphinx sphinx_rtd_theme sphinx-autodoc-typehints
```

Or install from project requirements:

```bash
pip install -r ../requirements.txt
```

### Building HTML Documentation

#### On Linux/macOS:

```bash
./make.sh html
```

#### On Windows:

```bash
make.bat html
```

#### Using Sphinx directly:

```bash
sphinx-build -b html source build/html
```

### Viewing Documentation

After building, open the generated HTML in your browser:

```bash
# On macOS
open build/html/index.html

# On Linux
xdg-open build/html/index.html

# On Windows
start build/html/index.html
```

## Documentation Structure

```
docs/
├── source/                 # Source files for documentation
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Main documentation page
│   ├── getting_started.rst # Getting started guide
│   ├── modules.rst        # Python API documentation
│   ├── contributing.rst   # Contributing guidelines
│   └── api/              # API documentation modules
├── build/                 # Generated documentation (created during build)
├── make.sh               # Build script for Linux/macOS
└── make.bat              # Build script for Windows
```

## Writing Documentation

### Adding New Pages

1. Create a new `.rst` file in `source/`
2. Add it to the `toctree` in `index.rst` or another appropriate file

### RST Syntax Quick Reference

- **Headings**: Use `=`, `-`, `~` for different levels
- **Bold**: `**text**`
- **Italic**: `*text*`
- **Code blocks**: Use `.. code-block::` directive
- **Links**: `` `Text <url>`_ ``
- **Internal references**: `` :ref:`label` ``

Example:

```rst
Section Title
=============

This is a paragraph.

.. code-block:: python

    def hello():
        print("Hello, World!")

See also :doc:`another_page`.
```

## Automatic API Documentation

The documentation automatically generates API docs from docstrings in your Python code.

Ensure your functions and classes have proper docstrings:

```python
def my_function(arg1, arg2):
    """Short description.

    Longer description of what the function does.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Example:
        >>> my_function("a", "b")
        "ab"
    """
    pass
```

## GitHub Actions Integration

The documentation is automatically built and deployed to GitHub Pages whenever you push to the main/master branch. See `.github/workflows/build-docs.yml` for the workflow configuration.

### Enabling GitHub Pages

To publish documentation to GitHub Pages:

1. Go to your GitHub repository settings
2. Navigate to "Pages" section
3. Set the source to "GitHub Actions"

The workflow will automatically deploy the built documentation.

## Troubleshooting

### Build fails with "sphinx: command not found"

Install Sphinx:

```bash
pip install sphinx sphinx_rtd_theme
```

### Module import errors

Ensure the `src/` directory is in the Python path. Check that `conf.py` correctly adds it:

```python
sys.path.insert(0, os.path.abspath('../../src'))
```

### Theme not found

Install the RTD theme:

```bash
pip install sphinx_rtd_theme
```

## More Information

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Guide](https://docutils.sourceforge.io/rst.html)
- [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)
