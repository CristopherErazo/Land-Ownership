#!/bin/bash

# This script runs the entire workflow: from extracting files to creating plots and launching the documentation server.

# Ask if the user wants to create plots or not

create_plots=$1


if [[ "$create_plots" == "y" ]]; then
    echo "Creating plots..."
    python ./scripts/europe_map_plots.py
    python ./scripts/box_plots.py
    echo "Plots created successfully."
else
    echo "Skipping plot creation."
fi

# Launch the documentation server from root directory using shphinx instead of make
echo "Building documentation..."
sphinx-build -b html docs docs/_build/html
echo "Documentation built successfully."

# Open the documentation in the default web browser
# start docs/_build/html/index.html
