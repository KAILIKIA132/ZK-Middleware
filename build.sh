#!/bin/bash

# Build script for ZK Middleware

echo "Building ZK Middleware..."
echo "========================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the zk_middleware directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install the package in development mode
echo "Installing package in development mode..."
pip install -e .

# Run tests if they exist
if [ -d "tests" ]; then
    echo "Running tests..."
    python -m pytest tests/
else
    echo "No tests directory found, skipping tests."
fi

echo "Build completed successfully!"
echo "To run the application, use: python app.py"
echo "To run with gunicorn, use: gunicorn -b 0.0.0.0:5000 app:app --workers 1 --timeout 120"