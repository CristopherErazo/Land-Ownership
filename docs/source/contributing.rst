Contributing
=============

We welcome contributions to the Land Ownership project! Here's how you can help:

Getting Started
---------------

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment and install dependencies:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -e ".[test]"
      pip install sphinx sphinx_rtd_theme

Development Workflow
---------------------

1. Create a feature branch:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. Make your changes and commit:

   .. code-block:: bash

      git commit -m "Description of your changes"

3. Push to your fork:

   .. code-block:: bash

      git push origin feature/your-feature-name

4. Create a pull request

Code Style
----------

* Follow PEP 8 conventions
* Use meaningful variable and function names
* Add docstrings to all functions and classes
* Write clear commit messages

Testing
-------

Run tests using pytest:

.. code-block:: bash

   pytest

Documentation
--------------

To build the documentation locally:

.. code-block:: bash

   cd docs
   make html

Then open ``build/html/index.html`` in your browser.

Reporting Issues
----------------

Please report bugs and issues on GitHub with:

* Clear description of the problem
* Steps to reproduce
* Expected behavior
* Actual behavior
* Environment details (Python version, OS, etc.)

Questions?
----------

Feel free to open a GitHub issue for questions or discussions about the project.
