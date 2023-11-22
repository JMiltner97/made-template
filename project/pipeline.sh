#!/bin/sh

# Install dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."

# Start data import
echo "Starting import:"
python3 /project/pipeline.py