#!/bin/bash
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$ROOT_DIR/venv"
fi

# Activate venv
source "$ROOT_DIR/venv/bin/activate"

# Install dependencies if needed (quietly)
pip install -q PyYAML openai

# Run the program
python3 "$ROOT_DIR/src/main.py"
