# Troubleshooting Guide

## Common Issues and Solutions

### 1. Device Connection Problems

**Symptom:** Unable to connect to SpeedFace M4 device
**Error:** "Failed to connect to ZK device"

**Solutions:**
- Verify device IP address and port (default 4370)
- Check network connectivity between middleware and device
- Ensure device is powered on and network cable is connected
- Check firewall settings on device and middleware host
- Verify no other application is using the device connection

### 2. Printer Connection Issues

**Symptom:** Printer not responding or printing garbled text
**Error:** "No printer available" or "Printing failed"

**Solutions:**
- Verify printer IP address and port (default 9100 for network printers)
- Check network connectivity to printer
- Ensure printer is powered on and has paper
- Verify printer supports ESC-POS commands
- Check printer driver compatibility

### 3. School API Integration Problems

**Symptom:** Payment status checks failing
**Error:** "School API call failed" or incorrect payment status

**Solutions:**
- Verify school API base URL is correct
- Check API key/token authentication
- Test API endpoint with curl or Postman
- Ensure middleware server can reach school API (firewall/VPN)
- Check API rate limiting or authentication expiration

### 4. Student ID Mismatch

**Symptom:** Student not found in school system
**Error:** "Student not found in database"

**Solutions:**
- Verify student enrollment in SpeedFace M4 device
- Check that user IDs in device match student IDs in school system
- Create ID mapping if systems use different ID formats
- Ensure students are properly enrolled in both systems

### 5. Docker Deployment Issues

**Symptom:** Container fails to start or connect to devices
**Error:** Various Docker-related errors

**Solutions:**
- Ensure Docker has network access to device and printer
- Check volume mounting for configuration files
- Verify port mappings in docker run command
- Check Docker logs for detailed error messages

## Testing Procedures

### 1. Device Connection Test
```bash
# Run the test script
python test_middleware.py
```

### 2. Printer Test
```bash
# Send test print command
curl -X POST http://localhost:5000/test-print \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Student", "id": "000", "details": "Test printing"}'
```

### 3. API Integration Test
```bash
# Test with mock server
python test_api.py mock

# In another terminal, test the API
python test_api.py
```

## Log Analysis

### Log Locations
- Application logs: stdout/stderr when running directly
- Docker logs: `docker logs <container_id>`
- System logs: `/var/log/syslog` or `/var/log/messages`

### Common Log Patterns
- `[INFO]` - Normal operation messages
- `[WARNING]` - Potential issues that don't stop operation
- `[ERROR]` - Errors that affect functionality
- `[CRITICAL]` - Severe errors that may stop the application

## Performance Tuning

### Polling Interval
Adjust the polling interval in app.py based on your needs:
- More frequent polling (3-5 seconds) for real-time response
- Less frequent polling (10-30 seconds) to reduce network load

### Connection Management
- The middleware maintains persistent connections to devices
- Connections are automatically re-established on failure
- Adjust timeout values in config.yml for your network conditions

## Security Considerations

### Network Security
- Restrict access to device management port (4370)
- Use VPN for remote access to middleware
- Implement firewall rules to limit device access

### Data Security
- Store configuration files with restricted permissions
- Use encrypted connections (HTTPS) to school API
- Regularly rotate API keys and authentication tokens

### Access Control
- Limit administrative access to authorized personnel only
- Use strong authentication for admin interface
- Regularly update software and dependencies