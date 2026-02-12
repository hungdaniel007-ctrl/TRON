#!/bin/bash
# Setup Virtual Environment Script
#
# This script creates a virtual environment for the documentation indexer system
# if it doesn't already exist, and installs the required dependencies.
#
# Author: Documentation Indexer System
# Version: 1.0.0
# License: MIT

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up virtual environment for Documentation Indexer..."

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH."
    exit 1
fi

# Check if virtualenv is available, install if not
if ! python3 -m venv --help &> /dev/null; then
    echo "Installing virtualenv..."
    python3 -m pip install --user --break-system-packages virtualenv || {
        echo "Error: Failed to install virtualenv."
        exit 1
    }
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR" || {
        echo "Error: Failed to create virtual environment."
        exit 1
    }
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists in $VENV_DIR."
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate" || {
    echo "Error: Failed to activate virtual environment."
    exit 1
}

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade --break-system-packages pip || {
    echo "Warning: Failed to upgrade pip, continuing..."
}

# Create requirements.txt if it doesn't exist
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Creating requirements.txt..."
    cat > "$REQUIREMENTS_FILE" << EOF
# Documentation Indexer Requirements
# Auto-generated requirements file

# Core dependencies
typing-extensions>=4.0.0
pathlib>=1.0.0

# Optional dependencies for enhanced functionality
# (Add any additional packages as needed)
EOF
    echo "Requirements file created: $REQUIREMENTS_FILE"
fi

# Install requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing requirements from $REQUIREMENTS_FILE..."
    pip install --break-system-packages -r "$REQUIREMENTS_FILE" || {
        echo "Warning: Failed to install some requirements, continuing..."
    }
else
    echo "No requirements.txt file found, skipping installation of dependencies."
fi

echo "Virtual environment setup completed successfully!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To run the documentation indexer scripts, use the wrapper scripts:"
echo "  ./run_extract.sh or ./run_verify.sh"