#!/bin/bash
# Environment setup script for ZK Middleware

echo "Setting up environment for ZK Middleware..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
echo "Found Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create default configuration file
if [ ! -f "config.yml" ]; then
    echo "Creating default configuration file..."
    cp config.example.yml config.yml
    echo "Please update config.yml with your specific settings."
fi

echo "Environment setup complete!"
echo "To activate the environment in the future, run: source venv/bin/activate"
echo "To start the application, run: python app.py"