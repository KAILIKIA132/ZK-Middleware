#!/usr/bin/env python3
"""
Post-deployment verification script
"""

import requests
import time
import os
import sys

def check_health_endpoint(base_url):
    """Check the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("✓ Health endpoint is working")
                return True
            else:
                print(f"✗ Health endpoint returned unexpected data: {data}")
                return False
        else:
            print(f"✗ Health endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint check failed: {e}")
        return False

def check_student_fees_endpoint(base_url):
    """Check the student fees endpoint"""
    try:
        response = requests.get(f"{base_url}/students/1/fees", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "paid" in data:
                print("✓ Student fees endpoint is working")
                return True
            else:
                print(f"✗ Student fees endpoint returned unexpected data: {data}")
                return False
        elif response.status_code == 404:
            print("⚠️  Student fees endpoint returned 404 (may be expected)")
            return True
        else:
            print(f"✗ Student fees endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Student fees endpoint check failed: {e}")
        return False

def check_test_print_endpoint(base_url):
    """Check the test print endpoint"""
    try:
        response = requests.post(
            f"{base_url}/test-print",
            json={"name": "Test Student", "id": "000", "details": "Test printing"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if "printed" in data:
                print("✓ Test print endpoint is working")
                return True
            else:
                print(f"✗ Test print endpoint returned unexpected data: {data}")
                return False
        else:
            print(f"✗ Test print endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Test print endpoint check failed: {e}")
        return False

def main():
    # Get the base URL from environment or use default
    base_url = os.environ.get("MIDDLEWARE_URL", "http://localhost:5000")
    
    print(f"Verifying middleware deployment at {base_url}...")
    print("=" * 50)
    
    # Wait a moment for the service to fully start
    print("Waiting for service to start...")
    time.sleep(5)
    
    tests = [
        ("Health Endpoint", lambda: check_health_endpoint(base_url)),
        ("Student Fees Endpoint", lambda: check_student_fees_endpoint(base_url)),
        ("Test Print Endpoint", lambda: check_test_print_endpoint(base_url))
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All post-deployment checks passed!")
        print("Your middleware is successfully deployed and working.")
    else:
        print("✗ Some checks failed.")
        print("Please check the logs and verify your deployment configuration.")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())