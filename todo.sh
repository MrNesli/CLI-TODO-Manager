#!/bin/bash

# Read bash script path from symbolic link
SOURCE_PATH="$(readlink -f /bin/todo)"

# Python script path
PYTHON_SCRIPT_PATH="$(dirname "${SOURCE_PATH}")/main.py"

# Pass CLI args to Python script
python3 "$PYTHON_SCRIPT_PATH" "$@"
