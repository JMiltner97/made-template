#!/bin/sh

# Install dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."

# Start data import
echo "Starting import:"
python pipeline.py

# Start import test
echo "Testing import:"
python pipeline_test.py