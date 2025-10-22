#!/bin/bash
# Startup script for ZK Middleware

# Check if config file exists
if [ ! -f "config.yml" ]; then
    echo "Error: config.yml not found!"
    echo "Please copy config.example.yml to config.yml and configure it."
    exit 1
fi

# Validate configuration
echo "Validating configuration..."
python validate_config.py
if [ $? -ne 0 ]; then
    echo "Configuration validation failed!"
    exit 1
fi

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Starting ZK Middleware in Docker container..."
    exec gunicorn -b 0.0.0.0:5000 app:app --workers 3
else
    echo "Starting ZK Middleware..."
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Install dependencies if not already installed
    if ! python -c "import flask" 2>/dev/null; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    # Start the application
    echo "Starting application..."
    python app.py
fi