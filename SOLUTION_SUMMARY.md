# ZKTeco SpeedFace M4 Canteen Management Solution

## Overview

This solution provides a complete middleware system that integrates a ZKTeco SpeedFace M4 biometric access device with a school management system via REST API for cafeteria access control. The system authenticates students via face recognition, verifies payment status, and either prints a meal ticket or displays an error message.

## Components

### 1. Hardware Requirements
- ZKTeco SpeedFace M4 biometric device
- Network thermal printer (ESC-POS compatible)
- Server/PC to run the middleware (Linux/Windows/macOS)
- Network infrastructure (switches, cables, etc.)

### 2. Software Components
- Python middleware application
- Flask web framework
- pyzk library for device communication
- python-escpos for printer control
- Docker for containerized deployment (optional)

## System Workflow

1. **Student Authentication**
   - Student approaches SpeedFace M4 device
   - Device captures face biometric and identifies student
   - Attendance log is generated with student ID

2. **Payment Verification**
   - Middleware polls device for new attendance logs
   - Extracts student ID from log entry
   - Queries school management system REST API
   - Verifies student's payment status for current meal

3. **Access Control**
   - If paid: 
     - Sends print job to thermal printer for meal ticket
     - Displays success message on device
   - If not paid:
     - Displays error message on device
     - Optionally prints denial ticket

4. **Logging and Monitoring**
   - All transactions are logged for auditing
   - Admin interface provides system status and recent activity

## Key Features

### Biometric Authentication
- Face recognition using SpeedFace M4 device
- Secure and contactless authentication
- Fast identification process

### Payment Integration
- Real-time verification with school management system
- REST API integration for payment status
- Configurable API authentication

### Ticket Printing
- Automatic ticket generation for authorized students
- ESC-POS compatible printer support
- Customizable ticket format

### Error Handling
- Clear error messages for unauthorized access
- Detailed logging for troubleshooting
- Automatic retry mechanisms

### Administration
- Web-based admin interface
- System status monitoring
- Test functions for printer and device

## Installation and Deployment

### Prerequisites
- Python 3.7 or higher
- Network access to SpeedFace M4 device
- Network access to thermal printer
- Access to school management system API

### Installation Steps
1. Clone the repository
2. Install dependencies with `pip install -r requirements.txt`
3. Configure settings in `config.example.yml`
4. Rename configuration file to `config.yml`
5. Run the application with `python app.py`

### Docker Deployment
1. Build image with `docker build -t zk-middleware:latest .`
2. Run container with `docker run -v $(pwd)/config.yml:/app/config.example.yml -p 5000:5000 zk-middleware:latest`

## Configuration

The system is configured through `config.yml`:

```yaml
device:
  ip: "192.168.1.100"      # SpeedFace M4 IP address
  port: 4370               # Device communication port
  timeout: 10              # Connection timeout

school_api:
  base_url: "https://school.example.com/api"  # School system API
  api_key: "YOUR_API_KEY"  # Authentication token

printer:
  type: "network"          # Printer type (network/local)
  network:
    host: "192.168.1.200"  # Printer IP address
    port: 9100             # Printer port

app:
  listen_host: "0.0.0.0"   # Middleware listen address
  listen_port: 5000        # Middleware port
```

## API Endpoints

- `GET /health` - System health check
- `POST /test-print` - Test printer functionality
- `POST /test-error` - Test error message printing
- `GET /admin` - Administration interface

## Security Considerations

- Use HTTPS for all API communications
- Store configuration files with restricted permissions
- Implement firewall rules to limit device access
- Regularly update dependencies and apply security patches

## Troubleshooting

Refer to `troubleshooting.md` for detailed troubleshooting guide including:
- Device connection issues
- Printer problems
- API integration errors
- Student ID mismatches
- Docker deployment issues

## Maintenance

- Regular log review and cleanup
- Monitor device and printer status
- Update student enrollments as needed
- Backup configuration files

## Support

For issues with this solution, please:
1. Check the troubleshooting guide
2. Review application logs
3. Verify all configuration settings
4. Contact the development team for assistance