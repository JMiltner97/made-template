#!/bin/sh
cd "$(dirname "$0")"

# Install dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed successfully."

# Start data import
echo "Starting import:"
python pipeline.py

# Start import test
echo "Testing import:"
python pipeline_test.py