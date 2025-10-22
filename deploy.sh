#!/bin/bash
# Deployment script for ZK Middleware

echo "Deploying ZK Middleware..."

# Create user if it doesn't exist
if ! id -u zkmiddleware >/dev/null 2>&1; then
    echo "Creating zkmiddleware user..."
    sudo useradd -r -s /bin/false zkmiddleware
fi

# Create installation directory
sudo mkdir -p /opt/zk-middleware
sudo chown zkmiddleware:zkmiddleware /opt/zk-middleware

# Copy files
echo "Copying application files..."
sudo cp -r ./* /opt/zk-middleware/
sudo chown -R zkmiddleware:zkmiddleware /opt/zk-middleware

# Create virtual environment and install dependencies
echo "Installing dependencies..."
cd /opt/zk-middleware
sudo -u zkmiddleware python3 -m venv venv
sudo -u zkmiddleware venv/bin/pip install -r requirements.txt

# Copy systemd service file
echo "Installing systemd service..."
sudo cp zk-middleware.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable zk-middleware.service
sudo systemctl start zk-middleware.service

echo "Deployment completed!"
echo "Check service status with: sudo systemctl status zk-middleware.service"