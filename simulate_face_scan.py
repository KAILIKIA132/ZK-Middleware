#!/usr/bin/env python3
"""
Script to simulate the complete face scanning workflow
This demonstrates how the system works when a student's face is scanned
"""

import requests
import json
import time
from datetime import datetime

# Configuration
MIDDLEWARE_URL = "http://localhost:5000"
MOCK_API_URL = "http://localhost:8080/api"
STUDENT_ID = "1001"  # Change to "1002" to test unpaid student

def simulate_face_scan(student_id):
    """Simulate the complete face scanning workflow"""
    print(f"=== Simulating Face Scan for Student ID: {student_id} ===")
    print()
    
    # Step 1: Simulate face scan creating an attendance log
    print("1. Face scanned at ZK device")
    timestamp = datetime.now().isoformat()
    attendance_data = {
        "student_id": student_id,
        "timestamp": timestamp,
        "device_id": "SpeedFace_M4_001"
    }
    
    try:
        # In a real system, the ZK device would send this directly
        # For simulation, we're sending it to our middleware
        response = requests.post(
            f"{MIDDLEWARE_URL}/attendance",
            headers={"Content-Type": "application/json"},
            json=attendance_data
        )
        print(f"   Attendance logged: {response.status_code}")
    except Exception as e:
        print(f"   Error logging attendance: {e}")
        return
    
    # Step 2: Check payment status (what the middleware does internally)
    print("\n2. Checking payment status with school API")
    try:
        # This is what the middleware does when it processes the log
        response = requests.get(f"{MIDDLEWARE_URL}/students/{student_id}/fees")
        if response.status_code == 200:
            payment_info = response.json()
            print(f"   Student: {payment_info.get('name', 'Unknown')}")
            print(f"   Paid: {payment_info.get('paid', False)}")
            print(f"   Details: {payment_info.get('details', 'No details')}")
        else:
            print(f"   Error checking payment: {response.status_code}")
            return
    except Exception as e:
        print(f"   Error checking payment: {e}")
        return
    
    # Step 3: Process based on payment status
    payment_info = response.json()
    if payment_info.get('paid', False):
        print("\n3. Student has paid - Processing meal ticket")
        
        # Print meal ticket
        ticket_data = {
            "student_id": student_id,
            "student_name": payment_info.get('name', 'Unknown Student'),
            "meal_type": "Lunch",
            "amount": payment_info.get('amount', 0.0)
        }
        
        try:
            response = requests.post(
                f"{MIDDLEWARE_URL}/print-ticket",
                headers={"Content-Type": "application/json"},
                json=ticket_data
            )
            if response.status_code == 200:
                print("   ✓ Meal ticket printed successfully")
            else:
                print(f"   ✗ Failed to print ticket: {response.json()}")
        except Exception as e:
            print(f"   ✗ Error printing ticket: {e}")
            
        # In a real system with ZK device, this would send a message to the device display
        print("   ✓ 'Access granted' message sent to device display")
        
    else:
        print("\n3. Student has NOT paid - Denying access")
        
        # Print error ticket
        try:
            error_data = {
                "message": "Fee not paid for today's meal"
            }
            response = requests.post(
                f"{MIDDLEWARE_URL}/test-error",
                headers={"Content-Type": "application/json"},
                json=error_data
            )
            if response.status_code == 200:
                print("   ✓ Error ticket printed")
            else:
                print(f"   ✗ Failed to print error ticket: {response.json()}")
        except Exception as e:
            print(f"   ✗ Error printing error ticket: {e}")
            
        # In a real system with ZK device, this would send a message to the device display
        print("   ✓ 'Fee unpaid. Contact admin.' message sent to device display")
    
    print("\n=== Workflow Complete ===")

def test_both_scenarios():
    """Test both paid and unpaid student scenarios"""
    print("Testing Paid Student (ID: 1001)")
    print("=" * 50)
    simulate_face_scan("1001")
    
    print("\n\nTesting Unpaid Student (ID: 1002)")
    print("=" * 50)
    simulate_face_scan("1002")

if __name__ == "__main__":
    print("ZK Middleware Face Scan Simulator")
    print("==================================")
    
    # Check if middleware is running
    try:
        response = requests.get(f"{MIDDLEWARE_URL}/health")
        if response.status_code != 200:
            print("ERROR: Middleware is not running. Please start the middleware first.")
            exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to middleware: {e}")
        print("Please ensure the middleware is running on port 5000")
        exit(1)
    
    # Check if mock API is running
    try:
        response = requests.get(f"{MOCK_API_URL}/health")
        if response.status_code != 200:
            print("ERROR: Mock API is not running. Please start the mock API first.")
            exit(1)
    except Exception as e:
        print(f"ERROR: Cannot connect to mock API: {e}")
        print("Please ensure the mock API is running on port 8080")
        exit(1)
    
    # Run simulation
    test_both_scenarios()