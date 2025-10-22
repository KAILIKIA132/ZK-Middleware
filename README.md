# ZK Middleware for Canteen Management System

A Python middleware that integrates ZKTeco SpeedFace M4 biometric devices with school management systems for cafeteria access control.

## Features

- **Biometric Integration**: Connects to ZKTeco SpeedFace M4 devices for face recognition
- **Payment Verification**: Integrates with school management systems via REST API
- **Ticket Printing**: Controls network thermal printers for meal tickets
- **Access Control**: Grants or denies cafeteria access based on payment status
- **Monitoring**: Provides real-time system status and logging
- **Web Interface**: Admin dashboard for system monitoring

## Prerequisites

- Python 3.9+
- ZKTeco SpeedFace M4 device
- Network thermal printer (ESC/POS compatible)
- Access to school management system API

## Installation

### Using pip

```bash
pip install -r requirements.txt
```

### Using Docker

```bash
docker build -t zk-middleware .
docker run -p 5000:5000 zk-middleware
```

## Configuration

Set the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEVICE_IP` | IP address of ZKTeco device | `192.168.1.100` |
| `DEVICE_PORT` | Port of ZKTeco device | `4370` |
| `DEVICE_TIMEOUT` | Connection timeout (seconds) | `10` |
| `SCHOOL_API_BASE_URL` | School management system API URL | `https://school.example.com/api` |
| `SCHOOL_API_KEY` | API key for school system | `REPLACE_WITH_SECRET` |
| `PRINTER_TYPE` | Printer type (`network` or `local`) | `network` |
| `PRINTER_HOST` | Printer IP address | `192.168.1.200` |
| `PRINTER_PORT` | Printer port | `9100` |
| `LISTEN_HOST` | Host to bind to | `0.0.0.0` |
| `PORT` | Port to listen on | `5000` |

## API Endpoints

- `GET /health` - System health check
- `GET /students/{id}/fees` - Check student payment status
- `POST /attendance` - Log attendance
- `POST /print-ticket` - Print meal ticket
- `POST /test-print` - Test printer
- `POST /test-error` - Test error printing
- `GET /admin` - Admin dashboard

## Deployment

### Render

1. Fork this repository
2. Create a new Web Service on Render
3. Set the root directory to `zk_middleware`
4. Use the following commands:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -b 0.0.0.0:10000 app:app --workers 1 --timeout 120`
5. Add environment variables as needed

### Docker

```bash
docker build -t zk-middleware .
docker run -d -p 5000:5000 \
  -e DEVICE_IP=192.168.1.100 \
  -e SCHOOL_API_BASE_URL=https://your-school-api.com/api \
  -e PRINTER_HOST=192.168.1.200 \
  zk-middleware
```

## Development

### Running locally

```bash
export PORT=5000
python app.py
```

### Running with Gunicorn

```bash
gunicorn -b 0.0.0.0:5000 app:app --workers 1 --timeout 120
```

## Testing

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.