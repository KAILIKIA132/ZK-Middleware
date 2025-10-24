#!/usr/bin/env python3
"""
Script to verify all endpoints in the ZK Middleware system are working correctly
"""

import requests
import json
from datetime import datetime

# Configuration
MIDDLEWARE_URL = "http://localhost:5000"
MOCK_API_URL = "http://localhost:8080/api"

def test_endpoint(url, method="GET", headers=None, data=None, description=""):
    """Test a single endpoint and report results"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
        print(f"{status} {description} - Status: {response.status_code}")
        return response.status_code < 400
    except Exception as e:
        print(f"❌ FAIL {description} - Error: {e}")
        return False

def verify_all_endpoints():
    """Verify all endpoints in the system"""
    print("ZK Middleware - Complete Endpoint Verification")
    print("=" * 50)
    
    results = []
    
    # System Health Checks
    print("\n1. SYSTEM HEALTH CHECKS")
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/health", "GET", None, None, "Middleware Health"))
    results.append(test_endpoint(f"{MOCK_API_URL}/health", "GET", None, None, "Mock API Health"))
    
    # Student Enrollment Management
    print("\n2. STUDENT ENROLLMENT MANAGEMENT")
    headers = {"Authorization": "Bearer test_api_key"}
    results.append(test_endpoint(f"{MOCK_API_URL}/students", "GET", headers, None, "Get All Students (Mock API)"))
    results.append(test_endpoint(f"{MOCK_API_URL}/students/1001/fees", "GET", headers, None, "Get Student 1001 (Mock API)"))
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/students/1001/fees", "GET", None, None, "Get Student 1001 (Middleware)"))
    results.append(test_endpoint(f"{MOCK_API_URL}/students/1002/fees", "GET", headers, None, "Get Student 1002 (Mock API)"))
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/students/1002/fees", "GET", None, None, "Get Student 1002 (Middleware)"))
    
    # Face Scanning Simulation
    print("\n3. FACE SCANNING SIMULATION")
    timestamp = datetime.now().isoformat()
    attendance_data_1001 = {
        "student_id": "1001",
        "timestamp": timestamp,
        "device_id": "SpeedFace_M4_001"
    }
    attendance_data_1002 = {
        "student_id": "1002",
        "timestamp": timestamp,
        "device_id": "SpeedFace_M4_001"
    }
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/attendance", "POST", {"Content-Type": "application/json"}, attendance_data_1001, "Simulate Face Scan - Student 1001"))
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/attendance", "POST", {"Content-Type": "application/json"}, attendance_data_1002, "Simulate Face Scan - Student 1002"))
    
    # Ticket Printing Functions
    print("\n4. TICKET PRINTING FUNCTIONS")
    ticket_data = {
        "student_id": "1001",
        "student_name": "Wangari Maathai",
        "meal_type": "Lunch",
        "amount": 150.00
    }
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/print-ticket", "POST", {"Content-Type": "application/json"}, ticket_data, "Print Meal Ticket"))
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/test-print", "POST", {"Content-Type": "application/json"}, {"name": "Test Student", "id": "001", "details": "Test printing"}, "Test Print"))
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/test-error", "POST", {"Content-Type": "application/json"}, {"message": "Test error message"}, "Test Error Print"))
    
    # Admin Functions
    print("\n5. ADMIN FUNCTIONS")
    results.append(test_endpoint(f"{MIDDLEWARE_URL}/admin", "GET", None, None, "Admin Dashboard"))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - System is fully operational!")
    else:
        print(f"⚠️  {total - passed} tests failed - Please check the system")
    
    return passed == total

def test_student_payment_status():
    """Test the critical payment status functionality"""
    print("\n6. PAYMENT STATUS VERIFICATION")
    print("-" * 30)
    
    test_students = [
        {"id": "1001", "name": "Wangari Maathai", "expected_paid": True},
        {"id": "1002", "name": "Jomo Kenyatta", "expected_paid": False},
        {"id": "1003", "name": "Chinua Achebe", "expected_paid": True},
        {"id": "1004", "name": "Grace Ogot", "expected_paid": True},
        {"id": "1005", "name": "Ngugi wa Thiong'o", "expected_paid": False}
    ]
    
    all_correct = True
    for student in test_students:
        try:
            # Test through middleware
            response = requests.get(f"{MIDDLEWARE_URL}/students/{student['id']}/fees")
            if response.status_code == 200:
                data = response.json()
                paid_status = data.get("paid", False)
                if paid_status == student["expected_paid"]:
                    status = "✅ CORRECT"
                else:
                    status = "❌ INCORRECT"
                    all_correct = False
                print(f"{status} {student['name']} (ID: {student['id']}) - Paid: {paid_status} (Expected: {student['expected_paid']})")
            else:
                print(f"❌ ERROR {student['name']} (ID: {student['id']}) - Status: {response.status_code}")
                all_correct = False
        except Exception as e:
            print(f"❌ ERROR {student['name']} (ID: {student['id']}) - Exception: {e}")
            all_correct = False
    
    if all_correct:
        print("\n🎉 ALL PAYMENT STATUS CHECKS CORRECT!")
    else:
        print("\n⚠️  SOME PAYMENT STATUS CHECKS FAILED!")
    
    return all_correct

if __name__ == "__main__":
    print("ZK Middleware Complete Verification Script")
    print("========================================")
    
    # Run all endpoint verification
    endpoints_ok = verify_all_endpoints()
    
    # Run payment status verification
    payment_ok = test_student_payment_status()
    
    # Final result
    print("\n" + "=" * 50)
    print("FINAL VERIFICATION RESULT")
    print("=" * 50)
    if endpoints_ok and payment_ok:
        print("🎉 COMPLETE SYSTEM VERIFICATION SUCCESSFUL!")
        print("✅ All endpoints working correctly")
        print("✅ All payment status connections working correctly")
        print("✅ System ready for enrollment and process testing")
    else:
        print("❌ SYSTEM VERIFICATION FAILED!")
        if not endpoints_ok:
            print("❌ Some endpoints are not working")
        if not payment_ok:
            print("❌ Payment status connections have issues")
        print("Please check the system and run verification again")