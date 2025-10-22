# ZK Middleware Deployment Guide

This guide provides detailed instructions for deploying the ZK Middleware to various environments.

## Prerequisites

Before deploying, ensure you have:

1. **Hardware Requirements**:
   - ZKTeco SpeedFace M4 device on the same network
   - Network thermal printer (ESC/POS compatible)
   - Server/PC to run the middleware

2. **Software Requirements**:
   - Python 3.9 or higher
   - Docker (optional, for containerized deployment)
   - Git (for cloning the repository)

3. **Network Requirements**:
   - Network connectivity between middleware and ZK device
   - Network connectivity between middleware and printer
   - Access to school management system API

## Deployment Options

### 1. Render (Recommended)

1. **Fork the Repository**:
   - Fork this repository to your GitHub account

2. **Create Web Service**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub account
   - Select your forked repository
   - Configure:
     - Name: `zk-middleware`
     - Environment: `Python`
     - Root Directory: `zk_middleware`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn -b 0.0.0.0:10000 app:app --workers 1 --timeout 120`
     - Plan: Free or paid as needed

3. **Configure Environment Variables**:
   - `DEVICE_IP`: IP address of your ZKTeco device
   - `SCHOOL_API_BASE_URL`: URL of your school management system API
   - `PRINTER_HOST`: IP address of your thermal printer
   - `PORT`: 10000 (Render will set this automatically)

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for build and deployment to complete
   - Note the assigned URL

### 2. Docker Deployment

1. **Build the Image**:
   ```bash
   cd zk_middleware
   docker build -t zk-middleware .
   ```

2. **Run the Container**:
   ```bash
   docker run -d \
     --name zk-middleware \
     -p 5000:5000 \
     -e DEVICE_IP=192.168.1.100 \
     -e SCHOOL_API_BASE_URL=https://your-school-api.com/api \
     -e PRINTER_HOST=192.168.1.200 \
     zk-middleware
   ```

3. **Verify Deployment**:
   ```bash
   curl http://localhost:5000/health
   ```

### 3. Direct Python Deployment

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd zk_middleware
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**:
   ```bash
   export DEVICE_IP=192.168.1.100
   export SCHOOL_API_BASE_URL=https://your-school-api.com/api
   export PRINTER_HOST=192.168.1.200
   export PORT=5000
   ```

5. **Run the Application**:
   ```bash
   # Using gunicorn (production)
   gunicorn -b 0.0.0.0:5000 app:app --workers 1 --timeout 120

   # Using development server
   python app.py
   ```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEVICE_IP` | IP address of ZKTeco device | `192.168.1.100` | Yes |
| `DEVICE_PORT` | Port of ZKTeco device | `4370` | No |
| `DEVICE_TIMEOUT` | Connection timeout (seconds) | `10` | No |
| `SCHOOL_API_BASE_URL` | School management system API URL | `https://school.example.com/api` | Yes |
| `SCHOOL_API_KEY` | API key for school system | `REPLACE_WITH_SECRET` | No |
| `PRINTER_TYPE` | Printer type (`network` or `local`) | `network` | No |
| `PRINTER_HOST` | Printer IP address | `192.168.1.200` | Yes |
| `PRINTER_PORT` | Printer port | `9100` | No |
| `LISTEN_HOST` | Host to bind to | `0.0.0.0` | No |
| `PORT` | Port to listen on | `5000` | Yes |

## Health Checks

The middleware provides a health check endpoint at `GET /health`:

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "ok"
}
```

## API Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the middleware is running
- **Response**: `{"status": "ok"}`

### Student Payment Status
- **Endpoint**: `GET /students/{id}/fees`
- **Description**: Check if a student has paid for meals
- **Response**: `{"paid": true, "details": "..."}`

### Attendance Logging
- **Endpoint**: `POST /attendance`
- **Description**: Log student attendance
- **Body**: `{"student_id": "...", "timestamp": "...", "device_id": "..."}`
- **Response**: `{"message": "Attendance logged successfully"}`

### Ticket Printing
- **Endpoint**: `POST /print-ticket`
- **Description**: Print a meal ticket
- **Body**: `{"student_id": "...", "student_name": "...", "meal_type": "...", "amount": 0.0}`
- **Response**: `{"message": "Ticket printed successfully"}`

### Test Printing
- **Endpoint**: `POST /test-print`
- **Description**: Test printer functionality
- **Body**: `{"name": "...", "id": "...", "details": "..."}`
- **Response**: `{"printed": true}`

### Test Error Printing
- **Endpoint**: `POST /test-error`
- **Description**: Test error message printing
- **Body**: `{"message": "..."}`
- **Response**: `{"printed": true}`

## Monitoring and Logging

The middleware logs important events to stdout/stderr. When deployed on Render, these logs are automatically captured and can be viewed in the Render dashboard.

### Log Levels
- **INFO**: General operational messages
- **WARNING**: Potential issues that don't stop operation
- **ERROR**: Errors that affect functionality
- **CRITICAL**: Severe errors that may stop the application

### Common Log Messages
- `Connected to ZK device`: Device connection established
- `Ticket printed for student`: Successful ticket printing
- `Student not paid`: Access denied due to unpaid fees
- `Polling loop error`: Device communication issues

## Troubleshooting

### Common Issues

1. **Device Connection Failed**:
   - Check `DEVICE_IP` and `DEVICE_PORT`
   - Verify network connectivity to the device
   - Ensure device is powered on

2. **Printer Not Working**:
   - Check `PRINTER_HOST` and `PRINTER_PORT`
   - Verify printer is connected and has paper
   - Test printer connectivity from the middleware server

3. **School API Integration Failing**:
   - Verify `SCHOOL_API_BASE_URL` and `SCHOOL_API_KEY`
   - Test API endpoint manually
   - Check for firewall restrictions

4. **Worker Boot Issues**:
   - Use single worker (`--workers 1`)
   - Increase timeout (`--timeout 120`)
   - Check logs for specific error messages

### Support

If you encounter issues with deployment:

1. Check the logs for error messages
2. Verify all environment variables are correctly set
3. Ensure network connectivity between services
4. Contact Render support for platform-specific issues