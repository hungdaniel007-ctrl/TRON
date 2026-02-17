#!/bin/bash
# Activate the uv virtual environment
source .venv/bin/activate
echo "Virtual environment activated. To deactivate, run 'deactivate'."
# Add commands to run your application here later

# Drop into a Python shell for debugging
python -c "import langgraph_checkpoint_sqlite; from langgraph_checkpoint_sqlite import SqliteSaver; print('Manual import successful!');"