#!/usr/bin/env python3
"""
Script to verify enrollment consistency across all systems
This simulates what would be checked in a real deployment
"""

import requests
import json

def verify_enrollment_consistency():
    """Verify that student IDs are consistent across all systems"""
    print("ZK Middleware Enrollment Consistency Verification")
    print("=" * 50)
    
    # In a real system, this would check:
    # 1. ZK Device enrolled users
    # 2. School system student records
    # 3. Middleware configuration
    
    # For simulation, we'll check our mock data
    print("1. Checking Mock School API Students")
    try:
        response = requests.get("http://localhost:8080/api/students", 
                              headers={"Authorization": "Bearer test_api_key"})
        if response.status_code == 200:
            students = response.json()
            print(f"   ✅ Found {len(students)} students in school system")
            
            # Display student information
            print("   Student List:")
            for student in students:
                print(f"     ID: {student['student_id']:<5} Name: {student['name']:<20} Paid: {student['paid']}")
        else:
            print(f"   ❌ Error accessing school API: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error accessing school API: {e}")
        return False
    
    print("\n2. Verifying Student ID Consistency")
    student_ids = ["1001", "1002", "1003", "1004", "1005"]
    
    all_consistent = True
    for student_id in student_ids:
        print(f"\n   Checking Student ID: {student_id}")
        
        # Check school API
        school_exists = False
        school_data = None
        try:
            school_response = requests.get(f"http://localhost:8080/api/students/{student_id}/fees",
                                         headers={"Authorization": "Bearer test_api_key"})
            school_exists = school_response.status_code == 200
            if school_exists:
                school_data = school_response.json()
                print(f"     School System: ✅ Exists - {school_data['name']}")
            else:
                print(f"     School System: ❌ Not found")
                all_consistent = False
        except Exception as e:
            print(f"     School System: ❌ Error - {e}")
            all_consistent = False
        
        # Check middleware
        try:
            middleware_response = requests.get(f"http://localhost:5000/students/{student_id}/fees")
            middleware_exists = middleware_response.status_code == 200
            if middleware_exists:
                middleware_data = middleware_response.json()
                print(f"     Middleware:    ✅ Exists - {middleware_data['name']}")
                
                # Verify data consistency
                if school_exists and school_data:
                    if school_data['name'] == middleware_data['name'] and school_data['paid'] == middleware_data['paid']:
                        print(f"     Data Consistency: ✅ Match")
                    else:
                        print(f"     Data Consistency: ❌ Mismatch")
                        all_consistent = False
            else:
                print(f"     Middleware:    ❌ Not found")
                all_consistent = False
        except Exception as e:
            print(f"     Middleware:    ❌ Error - {e}")
            all_consistent = False
    
    print("\n3. Testing Enrollment Workflow Simulation")
    print("   Simulating face scan for each enrolled student:")
    
    for student_id in student_ids:
        try:
            # This simulates what happens when a student's face is scanned
            response = requests.post("http://localhost:5000/attendance",
                                   json={
                                       "student_id": student_id,
                                       "timestamp": "2025-10-24T10:00:00",
                                       "device_id": "SpeedFace_M4_001"
                                   })
            if response.status_code == 201:
                print(f"     Student {student_id}: ✅ Attendance logged (face scan simulated)")
            else:
                print(f"     Student {student_id}: ❌ Failed to log attendance")
                all_consistent = False
        except Exception as e:
            print(f"     Student {student_id}: ❌ Error - {e}")
            all_consistent = False
    
    print("\n" + "=" * 50)
    if all_consistent:
        print("🎉 ALL ENROLLMENT CONSISTENCY CHECKS PASSED!")
        print("✅ Student IDs are consistent across all systems")
        print("✅ Enrollment data is properly synchronized")
        print("✅ System ready for face scanning workflows")
    else:
        print("❌ ENROLLMENT CONSISTENCY ISSUES FOUND!")
        print("❌ Please check student ID consistency between systems")
    
    return all_consistent

def show_enrollment_requirements():
    """Show what's needed for proper enrollment"""
    print("\nENROLLMENT REQUIREMENTS")
    print("=" * 25)
    print("For proper system operation, ensure:")
    print("")
    print("1. ZK DEVICE ENROLLMENT:")
    print("   - Each student's face enrolled with User ID")
    print("   - User ID matches school system ID exactly")
    print("   - High-quality face templates captured")
    print("")
    print("2. SCHOOL SYSTEM:")
    print("   - Student record exists for each enrolled user")
    print("   - Student ID format consistent with ZK device")
    print("   - Payment status up-to-date")
    print("")
    print("3. MIDDLEWARE CONFIGURATION:")
    print("   - School API URL correctly configured")
    print("   - API authentication working")
    print("   - Network connectivity to all systems")
    print("")
    print("4. INTEGRATION CHECKS:")
    print("   - Run this verification script regularly")
    print("   - Monitor for ID mismatches")
    print("   - Verify new enrollments immediately")

if __name__ == "__main__":
    print("ZK Middleware Enrollment Verification")
    print("====================================")
    
    # Check if services are running
    try:
        middleware_health = requests.get("http://localhost:5000/health")
        api_health = requests.get("http://localhost:8080/api/health")
        
        if middleware_health.status_code == 200 and api_health.status_code == 200:
            success = verify_enrollment_consistency()
            show_enrollment_requirements()
            
            if success:
                print("\n✅ System ready for enrollment testing!")
            else:
                print("\n❌ Please fix enrollment consistency issues before testing")
        else:
            print("❌ Services not running properly")
            print(f"  Middleware: {middleware_health.status_code if middleware_health else 'Unreachable'}")
            print(f"  API: {api_health.status_code if api_health else 'Unreachable'}")
            print("Please start both services before running verification")
    except Exception as e:
        print(f"❌ Cannot connect to services: {e}")
        print("Please ensure both the middleware (port 5000) and mock API (port 8080) are running")