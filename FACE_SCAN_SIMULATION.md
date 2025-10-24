# Face Scan Simulation

This document explains how to simulate and test the face scanning workflow for the ZK Middleware system.

## How the System Works

When a student's face is scanned at the ZK SpeedFace M4 device:

1. The device recognizes the student and creates an attendance log
2. The middleware polls the device for new logs (every 3 seconds)
3. For each new log:
   - Extracts the student ID
   - Checks payment status via the school API
   - If paid: Prints meal ticket and grants access
   - If unpaid: Prints error message and denies access

## Running the Simulation

### Prerequisites
1. ZK Middleware running on port 5000
2. Mock school API running on port 8080

### Running the Simulation Script
```bash
cd /Users/aaron/CanteenManagementSystem/zk_middleware
python simulate_face_scan.py
```

This will simulate both scenarios:
- Paid student (ID: 1001) - Should grant access and attempt to print ticket
- Unpaid student (ID: 1002) - Should deny access and print error ticket

## Sample Output

### For Paid Student (1001):
```
=== Simulating Face Scan for Student ID: 1001 ===

1. Face scanned at ZK device
   Attendance logged: 201

2. Checking payment status with school API
   Student: Wangari Maathai
   Paid: True
   Details: Lunch payment confirmed

3. Student has paid - Processing meal ticket
   ✗ Failed to print ticket: {'error': 'Failed to print ticket'}
   ✓ 'Access granted' message sent to device display

=== Workflow Complete ===
```

### For Unpaid Student (1002):
```
=== Simulating Face Scan for Student ID: 1002 ===

1. Face scanned at ZK device
   Attendance logged: 201

2. Checking payment status with school API
   Student: Jomo Kenyatta
   Paid: False
   Details: Lunch payment not found

3. Student has NOT paid - Denying access
   ✓ Error ticket printed
   ✓ 'Fee unpaid. Contact admin.' message sent to device display

=== Workflow Complete ===
```

## Understanding the Results

### Ticket Printing Failure
The "Failed to print ticket" message is expected in the local testing environment because:
- No physical printer is connected
- The printer configuration points to a network printer at 192.168.1.200:9100
- In production, this would connect to the actual thermal printer

### Access Control
The system correctly:
- Identifies paid vs unpaid students
- Follows the appropriate workflow for each case
- Sends the correct messages to the device display (simulated)

## Testing Individual Components

### Check Payment Status
```bash
curl -X GET http://localhost:5000/students/1001/fees
```

### Simulate Attendance Log
```bash
curl -X POST http://localhost:5000/attendance \
  -H "Content-Type: application/json" \
  -d '{"student_id": "1001", "timestamp": "2025-10-24T14:30:00", "device_id": "test_device"}'
```

### Test Manual Ticket Printing
```bash
curl -X POST http://localhost:5000/print-ticket \
  -H "Content-Type: application/json" \
  -d '{"student_id": "1001", "student_name": "Wangari Maathai", "meal_type": "Lunch", "amount": 150.00}'
```

## In Production

When deployed with actual hardware:
1. The ZK SpeedFace M4 device will automatically send attendance logs
2. The thermal printer at 192.168.1.200:9100 will print actual tickets
3. The device display will show real-time messages to students
4. All components will work together seamlessly

## Troubleshooting

### Middleware Not Running
- Ensure `python app.py` is running
- Check that environment variables are set:
  ```bash
  export SCHOOL_API_BASE_URL=http://localhost:8080/api
  export SCHOOL_API_KEY=test_api_key
  ```

### Mock API Not Running
- Ensure `python mock_school_api.py` is running
- Verify by accessing http://localhost:8080/api/health

### Connection Issues
- Check firewall settings
- Verify IP addresses in configuration
- Ensure all services are on the same network