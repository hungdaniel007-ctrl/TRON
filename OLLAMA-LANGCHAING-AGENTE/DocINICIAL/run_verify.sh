#!/bin/bash
# Wrapper script to run verify_index with automatic venv activation
#
# This script ensures the virtual environment is activated before running
# the verify_index script, making execution seamless.

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
VENV_DIR="venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate" || {
        echo "Error: Failed to activate virtual environment."
        exit 1
    }
    echo "Virtual environment activated: $VENV_DIR"
else
    echo "Warning: Virtual environment not found at $VENV_DIR, proceeding without activation..."
fi

# Check if the main script exists
MAIN_SCRIPT="doc_indexer/verify_index.py"
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "Error: Main script not found at $MAIN_SCRIPT"
    exit 1
fi

# Run the main script with all passed arguments
echo "Running verify_index with arguments: $@"
python "$MAIN_SCRIPT" "$@"

echo "Index verification completed successfully!"