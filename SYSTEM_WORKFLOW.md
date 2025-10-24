# ZK Middleware System Workflow

## Current Implementation

### 1. Face Scanning Process
1. Student approaches the ZK SpeedFace M4 device
2. Device captures and recognizes the student's face
3. Attendance log is created with student ID and timestamp

### 2. Middleware Processing
1. Middleware continuously polls the ZK device for new attendance logs (every 3 seconds)
2. For each new log entry:
   - Extract student ID from the log
   - Call the school API to check payment status
   - If paid:
     * Send "Access granted" message to device display
     * Print meal ticket/receipt
   - If unpaid:
     * Send "Fee unpaid" message to device display
     * Print error ticket

### 3. Ticket Printing
When a student is verified as paid, the system prints a meal ticket with:
- School name and "CAFETERIA"
- Student name and ID
- Meal details
- Timestamp
- "Thank you" message

## Suggested Enhancements

### 1. Improved Ticket Design
To include student images on the receipt, we would need to:
1. Store student photos in the school system
2. Modify the printer code to handle image printing
3. Update the ticket template

### 2. Real-time Processing
Instead of polling, implement a webhook or real-time notification system:
1. Configure ZK device to send instant notifications
2. Implement webhook endpoint in middleware
3. Process attendance immediately when received

### 3. Enhanced Error Handling
Improve the user experience for various scenarios:
1. Network connectivity issues
2. Printer offline status
3. Unknown student IDs
4. API timeouts

## Implementation Details

### Current API Endpoints
- `/students/{id}/fees` - Check payment status
- `/print-ticket` - Print meal ticket
- `/attendance` - Log attendance (for testing)

### Sample Payment Status Response
```json
{
  "student_id": "1001",
  "name": "Wangari Maathai",
  "grade": "Grade 8",
  "class": "8A",
  "paid": true,
  "details": "Lunch payment confirmed",
  "amount": 150.00,
  "balance": 0.00,
  "last_payment_date": "2025-10-20"
}
```

### Sample Ticket Content
```
CRAWFORD INTERNATIONAL
CAFETERIA
------------------------------
Student: Wangari Maathai
ID: 1001
Lunch - R150.00
Date: 2025-10-24 14:30:00
------------------------------
Thank you. Enjoy your meal!
```

## Testing the Workflow

### 1. With Paid Student (1001)
1. Face scan at device
2. Middleware gets log entry
3. API call confirms payment
4. Meal ticket is printed
5. Device shows "Access granted"

### 2. With Unpaid Student (1002)
1. Face scan at device
2. Middleware gets log entry
3. API call shows unpaid status
4. Error ticket is printed
5. Device shows "Fee unpaid"

## Local Testing Without Hardware

Since you don't have the physical ZK device, you can test the workflow using:

### 1. Simulate Attendance Logging
```bash
curl -X POST http://localhost:5000/attendance \
  -H "Content-Type: application/json" \
  -d '{"student_id": "1001", "timestamp": "2025-10-24T14:30:00", "device_id": "test_device"}'
```

### 2. Test Ticket Printing
```bash
curl -X POST http://localhost:5000/print-ticket \
  -H "Content-Type: application/json" \
  -d '{"student_id": "1001", "student_name": "Wangari Maathai", "meal_type": "Lunch", "amount": 150.00}'
```

### 3. Check Payment Status
```bash
curl -X GET http://localhost:5000/students/1001/fees
```

## Adding Student Images to Tickets

To print student images on tickets, you would need to:

1. Modify the school API to include image URLs:
```json
{
  "student_id": "1001",
  "name": "Wangari Maathai",
  "photo_url": "http://school.example.com/photos/1001.jpg",
  "paid": true,
  "details": "Lunch payment confirmed"
}
```

2. Update the printer code to download and print images:
```python
# In printer.py
def print_ticket(self, student_name, student_id, details, photo_url=None):
    if photo_url:
        # Download and print student photo
        # (Implementation depends on printer capabilities)
        pass
```

3. Ensure the printer supports image printing (many ESC/POS printers do)

## Next Steps

1. Test the current implementation with the mock data
2. Consider implementing the image printing feature
3. Set up proper error handling and logging
4. Configure the actual ZK device when available