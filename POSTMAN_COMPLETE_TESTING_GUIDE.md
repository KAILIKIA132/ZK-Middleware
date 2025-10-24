# Complete Postman Testing Guide for ZK Middleware

This guide explains how to use the updated Postman collection to test all enrollments and processes in the ZK Middleware system.

## Prerequisites

1. [Postman](https://www.postman.com/downloads/) installed
2. ZK Middleware running on port 5000
3. Mock school API running on port 8080

## Starting the Services

### 1. Start the Mock School API
```bash
cd /Users/aaron/CanteenManagementSystem/zk_middleware
python mock_school_api.py
```

### 2. Start the ZK Middleware
```bash
cd /Users/aaron/CanteenManagementSystem/zk_middleware
export SCHOOL_API_BASE_URL=http://localhost:8080/api
export SCHOOL_API_KEY=test_api_key
python app.py
```

## Importing the Postman Collection

1. Open Postman
2. Click "Import" in the top left
3. Select the `ZK_Middleware_Complete_Testing.postman_collection.json` file
4. Click "Import"

## Collection Structure

The collection is organized into the following folders:

### 1. System Health Checks
- **Middleware Health Check**: Verify middleware is running
- **Mock API Health Check**: Verify mock API is running

### 2. Student Enrollment Management
- **Get All Students (Mock API)**: List all enrolled students
- **Get Student by ID (Mock API)**: Check student details directly in school system
- **Get Student by ID (Middleware)**: Check student details through middleware

### 3. Face Scanning Simulation
- **Simulate Face Scan - Log Attendance**: Generic attendance logging endpoint
- **Simulate Face Scan - Paid Student (1001)**: Test with Wangari Maathai
- **Simulate Face Scan - Unpaid Student (1002)**: Test with Jomo Kenyatta

### 4. Ticket Printing Functions
- **Print Meal Ticket**: Print a meal ticket for any student
- **Test Print**: Test basic printer functionality
- **Test Error Print**: Test error message printing

### 5. Admin Functions
- **Admin Dashboard**: Access the admin interface

### 6. Complete Workflow Tests
- **Full Process - Paid Student**: End-to-end test for paid student
- **Full Process - Unpaid Student**: End-to-end test for unpaid student

## Available Student IDs for Testing

The mock API includes the following sample students:

| Student ID | Name | Grade | Class | Paid Status |
|------------|------|-------|-------|-------------|
| 1001 | Wangari Maathai | Grade 8 | 8A | ✅ Paid |
| 1002 | Jomo Kenyatta | Grade 7 | 7B | ❌ Unpaid |
| 1003 | Chinua Achebe | Grade 9 | 9C | ✅ Paid |
| 1004 | Grace Ogot | Grade 6 | 6A | ✅ Paid |
| 1005 | Ngugi wa Thiong'o | Grade 10 | 10B | ❌ Unpaid |

## Testing Scenarios

### 1. Basic System Health
1. Run "Middleware Health Check" - Should return `{"status":"ok"}`
2. Run "Mock API Health Check" - Should return health status

### 2. Student Enrollment Verification
1. Run "Get All Students (Mock API)" - Should list all 5 students
2. Run "Get Student by ID (Mock API)" with student_id = 1001 - Should show Wangari's details
3. Run "Get Student by ID (Middleware)" with student_id = 1001 - Should return same data

### 3. Face Scanning Process
1. Run "Simulate Face Scan - Paid Student (1001)" - Should log attendance
2. Run "Simulate Face Scan - Unpaid Student (1002)" - Should log attendance
3. Try with different student IDs using "Simulate Face Scan - Log Attendance" and variables

### 4. Ticket Printing Functions
1. Run "Print Meal Ticket" with different student data
2. Run "Test Print" to verify printer connection
3. Run "Test Error Print" to verify error printing

### 5. Complete Workflow Testing
1. Run "Full Process - Paid Student" - Tests entire workflow for paid student
2. Run "Full Process - Unpaid Student" - Tests entire workflow for unpaid student

## Using Variables

The collection includes variables for easy testing:

- `{{student_id}}` - Default: "1001"
- `{{student_name}}` - Default: "Wangari Maathai"
- `{{amount}}` - Default: "150.00"

To change these:
1. Click on the collection name
2. Go to "Variables" tab
3. Modify the values as needed

## Testing Different Scenarios

### Test All Paid Students
1. Set `{{student_id}}` to "1001", "1003", or "1004"
2. Run "Simulate Face Scan - Log Attendance"
3. Observe that access is granted

### Test All Unpaid Students
1. Set `{{student_id}}` to "1002" or "1005"
2. Run "Simulate Face Scan - Log Attendance"
3. Observe that access is denied

### Test Unknown Students
1. Set `{{student_id}}` to any number not in the list (e.g., "9999")
2. Run "Simulate Face Scan - Log Attendance"
3. Observe the handling of unknown students

## Automated Testing with Postman Scripts

The "Complete Workflow Tests" folder includes automated tests:

1. **Full Process - Paid Student**: 
   - Sends attendance log
   - Verifies successful response (201 status)
   - Confirms success message

2. **Full Process - Unpaid Student**:
   - Sends attendance log
   - Verifies successful response (201 status)
   - Confirms success message

To run these tests:
1. Click on the test request
2. Click "Send"
3. Check the "Test Results" tab for results

## Monitoring System Logs

While testing, monitor the terminal output of both services:

### Middleware Logs
Shows:
- Attendance logging
- Payment status checks
- Ticket printing attempts
- Access decisions

### Mock API Logs
Shows:
- Incoming requests
- Requested student IDs
- Response data

## Troubleshooting

### Common Issues

1. **Services Not Running**
   - Error: "Could not get any response"
   - Solution: Ensure both middleware and mock API are running

2. **Wrong Student ID**
   - Error: 404 status
   - Solution: Use valid student IDs (1001-1005)

3. **Printer Not Connected**
   - Response: `{"printed": false, "error": "Printer not available"}`
   - Solution: Expected in local testing environment

### Verification Commands

Check if services are running:
```bash
# Check middleware
curl http://localhost:5000/health

# Check mock API
curl http://localhost:8080/api/health
```

## Advanced Testing

### 1. Performance Testing
- Use Postman's Collection Runner to run multiple requests
- Monitor response times
- Check for consistency

### 2. Stress Testing
- Send multiple simultaneous requests
- Verify system handles concurrent access

### 3. Edge Case Testing
- Test with invalid student IDs
- Test with malformed JSON data
- Test with missing required fields

This comprehensive testing collection allows you to verify every aspect of the ZK Middleware system, from basic enrollment management to complete face scanning workflows.