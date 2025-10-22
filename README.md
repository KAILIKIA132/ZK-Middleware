# ZKTeco SpeedFace M4 Middleware

A Python middleware that integrates a ZKTeco SpeedFace M4 biometric access device with a school management system via REST API. The system scans student faces, checks payment status, prints tickets for paid students, and shows errors for unpaid students.

## Features

- Connects to ZKTeco SpeedFace M4 device via TCP/IP
- Polls device for attendance/logs or uses live capture
- Verifies student payment status via REST API
- Prints tickets for students who have paid
- Displays error messages for students who haven't paid
- Dockerized for easy deployment

## Requirements

- Python 3.7+
- ZKTeco SpeedFace M4 device on the same network
- Network thermal printer supporting ESC-POS
- School management system with REST API

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application by copying `config.example.yml` to `config.yml` and updating the values:
   ```yaml
   device:
     ip: "192.168.1.100"  # IP of your SpeedFace M4 device
     port: 4370
     timeout: 10

   school_api:
     base_url: "https://school.example.com/api"
     api_key: "YOUR_API_KEY"

   printer:
     type: "network"  # or "local"
     network:
       host: "192.168.1.200"  # IP of your thermal printer
       port: 9100

   app:
     listen_host: "0.0.0.0"
     listen_port: 5000
   ```

## Usage

### Running locally

```bash
python app.py
```

### Running with Docker

```bash
docker build -t zk-middleware:latest .
docker run -v $(pwd)/config.yml:/app/config.example.yml -p 5000:5000 zk-middleware:latest
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /test-print` - Test printing functionality
- `POST /test-error` - Test error message printing

## How it works

1. The middleware connects to the SpeedFace M4 device
2. It polls the device for attendance logs or uses live capture
3. When a face is scanned, it extracts the student ID
4. It queries the school management system's REST API to check payment status
5. If paid:
   - Prints a ticket on the thermal printer
   - Optionally displays success message on device
6. If not paid:
   - Displays error message on device
   - Optionally prints error ticket

## Device Setup

Ensure students are enrolled in the SpeedFace M4 device with user IDs that match the school management system's student IDs.

## Troubleshooting

- Ensure the device IP and port are correct (default is 4370)
- Check network connectivity between middleware and device
- Verify school API endpoint and authentication
- Confirm printer connectivity and ESC-POS compatibility

## Security Considerations

- Run the middleware on a secure network
- Protect the school API with proper authentication
- Limit access to the device management port
- Store configuration files securely