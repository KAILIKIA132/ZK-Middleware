# Face Scan Workflow: What Happens When a Student's Fees Are Paid

## Overview

When a student approaches the ZK SpeedFace M4 biometric device and their face is scanned, the system performs several steps to determine access and print a meal card/receipt. Here's exactly what happens in each scenario:

## When Student Fees Are PAID ("paid": true)

### 1. Face Recognition
- Student's face is captured and recognized by the ZK device
- Student ID is identified from the enrolled templates
- Attendance log is created with timestamp

### 2. Log Processing by Middleware
- Middleware polls the device and retrieves the new attendance log
- Student ID is extracted from the log entry
- Middleware calls the school API to check payment status

### 3. Payment Verification
- API returns: `{"paid": true, "details": "Lunch payment confirmed", ...}`
- Middleware confirms student has paid required fees

### 4. Access Granted Actions
- **Device Display**: Shows "Access granted - Ticket printed" message
- **Ticket Printing**: Prints a meal card/receipt with:
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
- **System Logging**: Transaction is logged for reporting

### 5. Student Experience
- Green light or checkmark appears on device screen
- Student receives printed meal ticket
- Student proceeds to cafeteria line

## When Student Fees Are NOT Paid ("paid": false)

### 1. Face Recognition
- Same as paid scenario - face is recognized and ID extracted

### 2. Log Processing by Middleware
- Same as paid scenario - log is retrieved and processed

### 3. Payment Verification
- API returns: `{"paid": false, "details": "Lunch payment not found", ...}`
- Middleware determines student has not paid fees

### 4. Access Denied Actions
- **Device Display**: Shows "Fee unpaid. Contact admin." message
- **Error Printing**: Prints an error receipt with:
  ```
  ACCESS DENIED
  ------------------------------
  Fee not paid for today's meal
  ------------------------------
  Please contact administration.
  ```
- **System Logging**: Transaction is logged for follow-up

### 5. Student Experience
- Red light or X appears on device screen
- Student receives error ticket
- Student is directed to administration office

## Technical Implementation Details

### API Endpoints Used
1. **Internal**: `/students/{id}/fees` - Checks payment status
2. **External**: Configured school API endpoint - Returns payment data

### Response Processing
```python
# Simplified logic from app.py
res = check_payment(student_id)
if res.get("paid"):
    # Print meal ticket
    printer.print_ticket(student_name, student_id, details)
    zk.send_display_message("Access granted - Ticket printed")
else:
    # Print error message
    zk.send_display_message("Fee unpaid. Contact admin.")
    printer.print_error("Fee not paid for today's meal")
```

### Data Flow
```
Face Scan → ZK Device → Attendance Log → Middleware 
  → School API (Payment Check) → Decision → Actions
```

## Local Testing Results

When we tested with our mock data:

### Paid Student (1001 - Wangari Maathai)
- System correctly identified as paid
- Attempted to print meal ticket (failed due to no physical printer)
- Would show "Access granted" on device display

### Unpaid Student (1002 - Jomo Kenyatta)
- System correctly identified as unpaid
- Printed error ticket (simulated)
- Would show "Fee unpaid" on device display

## Production Environment Differences

In a real deployment:

1. **Physical Printer**: Tickets would actually print on thermal printer
2. **Real Device**: ZK SpeedFace M4 would show visual feedback
3. **Network Integration**: All components would communicate over network
4. **Database Storage**: Transactions would be stored for reporting
5. **Admin Dashboard**: Real-time monitoring of all transactions

## Key Features

1. **Instant Verification**: Payment status checked in real-time
2. **Automated Access Control**: No manual intervention required
3. **Physical Receipts**: Students receive printed proof of transaction
4. **Audit Trail**: All transactions logged for reporting
5. **Immediate Feedback**: Students know result immediately
6. **Scalable**: Can handle hundreds of students per hour

This system ensures only students with paid fees can access the cafeteria while providing a seamless experience for those who are paid up.