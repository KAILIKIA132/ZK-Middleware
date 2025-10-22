#!/bin/bash

# Startup script for ZK Middleware

echo "Starting ZK Middleware..."
echo "======================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the zk_middleware directory."
    exit 1
fi

# Set default environment variables if not already set
export PORT=${PORT:-5000}
export DEVICE_IP=${DEVICE_IP:-192.168.1.100}
export SCHOOL_API_BASE_URL=${SCHOOL_API_BASE_URL:-https://school.example.com/api}
export PRINTER_HOST=${PRINTER_HOST:-192.168.1.200}

echo "Environment variables:"
echo "  PORT: $PORT"
echo "  DEVICE_IP: $DEVICE_IP"
echo "  SCHOOL_API_BASE_URL: $SCHOOL_API_BASE_URL"
echo "  PRINTER_HOST: $PRINTER_HOST"

# Check if running in Docker
if [ -f /.dockerenv ]; then
    echo "Running in Docker container"
    exec gunicorn -b 0.0.0.0:$PORT app:app --workers 1 --timeout 120
else
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Check if dependencies are installed
    if ! python -c "import flask" 2>/dev/null; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    fi
    
    echo "Starting application..."
    if command -v gunicorn &> /dev/null; then
        echo "Using gunicorn..."
        gunicorn -b 0.0.0.0:$PORT app:app --workers 1 --timeout 120
    else
        echo "Using development server..."
        python app.py
    fi
fi