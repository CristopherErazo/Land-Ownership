Getting Started
===============

Installation
------------

Prerequisites
~~~~~~~~~~~~~

* Python 3.8 or higher
* pip or conda package manager

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone <repository-url>
      cd land_ownership

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the package in development mode:

   .. code-block:: bash

      pip install -e .
      pip install -r requirements.txt

4. Install optional dependencies for testing:

   .. code-block:: bash

      pip install -e ".[test]"

Project Structure
-----------------

.. code-block:: text

   land_ownership/
   ├── data/              # Data files (farm_subsidy data for 2023-2024)
   ├── docs/              # Documentation
   ├── notebooks/         # Jupyter notebooks for analysis
   ├── scripts/           # Standalone Python scripts
   ├── shell/             # Shell scripts for data processing
   ├── src/               # Source code
   │   └── land_ownership/
   │       └── configurations/
   ├── requirements.txt   # Python dependencies
   └── pyproject.toml     # Project metadata

Data
----

The project includes farm subsidy data from 2023 and 2024 for multiple European countries stored in CSV format.

**Available Countries:**
AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GB, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SK

Quick Start
-----------

1. Explore the notebooks:

   .. code-block:: bash

      jupyter notebook notebooks/

2. Run the main analysis script:

   .. code-block:: bash

      python scripts/main.py

3. View the shell scripts for data management:

   .. code-block:: bash

      # Download data
      bash shell/download_gdrive.sh
      
      # Extract data
      bash shell/extract_files.sh

Configuration
-------------

The project uses configuration files located in ``src/configurations/``:

* ``data_config.py`` - Data processing configuration
* ``plot_config.py`` - Plotting and visualization configuration

More Information
----------------

For more details about the project modules and API, see the :doc:`modules` documentation.

To contribute to the project, see :doc:`contributing`.
