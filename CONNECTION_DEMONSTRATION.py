#!/usr/bin/env python3
"""
Demonstration script showing exactly how the face scanning connects to fee payment status
"""

import requests
import json

def demonstrate_connection():
    """Show step by step how face scanning connects to payment status"""
    
    print("=" * 60)
    print("FACE SCANNING TO FEE PAYMENT STATUS CONNECTION")
    print("=" * 60)
    
    # Step 1: Simulate face enrollment (this would happen once per student)
    print("\n1. STUDENT ENROLLMENT (One-time setup)")
    print("   Student: Wangari Maathai")
    print("   Face scanned and stored in ZK device")
    print("   Assigned Student ID: 1001")
    print("   → ZK Device stores: {face_template: '...', user_id: '1001'}")
    
    # Step 2: Simulate daily face scan
    print("\n2. DAILY FACE SCANNING")
    print("   Wangari approaches ZK device")
    print("   Camera captures face")
    print("   System matches face to enrolled template")
    print("   ← ZK Device returns: {user_id: '1001', timestamp: '2025-10-24 14:30:00'}")
    
    # Step 3: Show how middleware extracts ID
    print("\n3. MIDDLEWARE PROCESSING")
    print("   Middleware receives attendance log")
    student_id = "1001"
    print(f"   Extracts Student ID: {student_id}")
    
    # Step 4: Show payment check
    print("\n4. PAYMENT STATUS CHECK")
    print(f"   Middleware calls: GET http://localhost:8080/api/students/{student_id}/fees")
    
    # Actually make the call to show it works
    try:
        response = requests.get(f"http://localhost:8080/api/students/{student_id}/fees", 
                              headers={"Authorization": "Bearer test_api_key"})
        if response.status_code == 200:
            payment_data = response.json()
            print(f"   ← School API returns: {json.dumps(payment_data, indent=2)}")
            
            # Step 5: Show decision making
            print("\n5. DECISION MAKING")
            if payment_data.get("paid"):
                print(f"   Decision: Student {payment_data['name']} (ID: {student_id}) HAS PAID")
                print("   Action: Grant access and print meal ticket")
            else:
                print(f"   Decision: Student {payment_data['name']} (ID: {student_id}) HAS NOT PAID")
                print("   Action: Deny access and print error message")
        else:
            print(f"   Error: {response.status_code}")
    except Exception as e:
        print(f"   Connection error: {e}")
    
    # Step 6: Show the complete link
    print("\n6. THE COMPLETE CONNECTION")
    print("   FACE SCAN → STUDENT ID → PAYMENT CHECK → DECISION")
    print("       ↓           ↓            ↓            ↓")
    print("   Wangari's    '1001'     API Call     Access Granted")
    print("    Face                   Success      Ticket Printed")
    print("")
    print("   This is the exact process the system performs!")
    
    # Show with unpaid student too
    print("\n" + "=" * 60)
    print("EXAMPLE WITH UNPAID STUDENT")
    print("=" * 60)
    
    unpaid_student_id = "1002"
    print(f"\nSame process for Student ID: {unpaid_student_id} (Jomo Kenyatta)")
    print(f"   Middleware calls: GET http://localhost:8080/api/students/{unpaid_student_id}/fees")
    
    try:
        response = requests.get(f"http://localhost:8080/api/students/{unpaid_student_id}/fees", 
                              headers={"Authorization": "Bearer test_api_key"})
        if response.status_code == 200:
            payment_data = response.json()
            print(f"   ← School API returns: {json.dumps(payment_data, indent=2)}")
            
            print("\nDecision:")
            if payment_data.get("paid"):
                print(f"   Student {payment_data['name']} HAS PAID → Grant access")
            else:
                print(f"   Student {payment_data['name']} HAS NOT PAID → Deny access")
    except Exception as e:
        print(f"   Connection error: {e}")

if __name__ == "__main__":
    print("ZK Middleware Connection Demonstration")
    print("Showing exactly how face scanning connects to fee payment status")
    
    # Verify services are running
    try:
        middleware_health = requests.get("http://localhost:5000/health")
        api_health = requests.get("http://localhost:8080/api/health")
        
        if middleware_health.status_code == 200 and api_health.status_code == 200:
            demonstrate_connection()
        else:
            print("ERROR: Services not running properly")
            print(f"  Middleware: {middleware_health.status_code}")
            print(f"  API: {api_health.status_code}")
    except Exception as e:
        print(f"ERROR: Cannot connect to services: {e}")
        print("Please ensure both the middleware (port 5000) and mock API (port 8080) are running")