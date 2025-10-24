#!/usr/bin/env python3
"""
Demo script showing the complete workflow with image printing
"""

import requests
import json
import time

def demo_complete_workflow():
    """Demonstrate the complete workflow with image printing"""
    
    print("KENYA SCHOOL MEAL PROGRAM")
    print("Complete Workflow Demo with Image Printing")
    print("=" * 50)
    
    # Step 1: Check student payment status (what happens during face scan)
    print("\n1. Checking student payment status...")
    try:
        response = requests.get("http://localhost:8080/api/students/1001/fees", 
                              headers={"Authorization": "Bearer test_api_key"})
        if response.status_code == 200:
            student_data = response.json()
            print(f"   Student: {student_data['name']}")
            print(f"   ID: {student_data['student_id']}")
            print(f"   Paid: {student_data['paid']}")
            print(f"   Photo URL: {student_data['photo_url']}")
        else:
            print(f"   Error: {response.status_code}")
            return
    except Exception as e:
        print(f"   Connection error: {e}")
        return
    
    # Step 2: Simulate face scan
    print("\n2. Simulating face scan...")
    try:
        response = requests.post("http://localhost:5000/attendance",
                               json={
                                   "student_id": "1001",
                                   "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                                   "device_id": "SpeedFace_M4_001"
                               })
        if response.status_code == 201:
            print("   ✅ Face scan simulated successfully")
            print("   🔄 Middleware processing attendance log...")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        return
    
    # Step 3: Show what the middleware does
    print("\n3. Middleware processing steps:")
    print("   🔍 Extracting student ID from attendance log")
    print("   🌐 Calling school API for payment status")
    print("   📋 Checking if student has paid fees")
    if student_data['paid']:
        print("   ✅ Student has paid - Printing meal card with image")
    else:
        print("   ❌ Student has not paid - Printing error card with image")
    
    # Step 4: Test manual printing with image
    print("\n4. Testing manual meal card printing with image...")
    try:
        response = requests.post("http://localhost:5000/print-ticket",
                               json={
                                   "student_id": student_data['student_id'],
                                   "student_name": student_data['name'],
                                   "meal_type": "Lunch",
                                   "amount": student_data['amount'],
                                   "photo_url": student_data['photo_url']
                               })
        if response.status_code == 200:
            print("   ✅ Meal card printed successfully with student image")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
    
    # Step 5: Show final result
    print("\n5. Final Result:")
    if student_data['paid']:
        print("   🎉 Student granted access to cafeteria")
        print("   🍽️  Meal card printed with student photo")
        print("   👍 Positive experience for student")
    else:
        print("   ⛔ Student denied access to cafeteria")
        print("   📄 Error card printed with student photo")
        print("   👎 Student directed to administration")
    
    print("\n" + "=" * 50)
    print("🎉 COMPLETE WORKFLOW DEMONSTRATION FINISHED")
    print("✅ Face scanning with image printing is working!")
    
    # Show sample of what gets printed
    print("\n📄 Sample Printed Card Layout:")
    print("""
        KENYA SCHOOL MEAL PROGRAM
           Ministry of Education
        ------------------------------
            SCHOOL MEAL CARD
        ==============================

            [STUDENT IMAGE]
            (100x100 pixels)

        Student Name: Wangari Maathai
        Student ID:   1001
        Meal Type:    Lunch - KES 150.00
        Date:         2025-10-24 13:52:35

                STATUS: AUTHORIZED
                   ✔ MEAL APPROVED

        "Education is the most powerful weapon
         which you can use to change the world."
         - Nelson Mandela

        ==============================
           Enjoy your nutritious meal!
              Harambee! (Pull together)
        ________________________________
    """)

if __name__ == "__main__":
    # Check if services are running
    try:
        middleware_health = requests.get("http://localhost:5000/health")
        api_health = requests.get("http://localhost:8080/api/health")
        
        if middleware_health.status_code == 200 and api_health.status_code == 200:
            demo_complete_workflow()
        else:
            print("❌ Services not running properly")
            print(f"  Middleware: {middleware_health.status_code if middleware_health else 'Unreachable'}")
            print(f"  API: {api_health.status_code if api_health else 'Unreachable'}")
            print("Please start both services before running demo")
    except Exception as e:
        print(f"❌ Cannot connect to services: {e}")
        print("Please ensure both the middleware (port 5000) and mock API (port 8080) are running")