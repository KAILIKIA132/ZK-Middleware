#!/usr/bin/env python3
"""
Test script for deployment verification
"""

import requests
import time
import os

def test_middleware_health():
    """Test middleware health endpoint"""
    try:
        # Try localhost first
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Local middleware health check: {data}")
            return True
    except Exception as e:
        print(f"Local middleware not available: {e}")
    
    # Try Render URL if available
    render_url = os.environ.get('RENDER_MIDDLEWARE_URL', 'https://canteen-middleware.onrender.com')
    try:
        response = requests.get(f'{render_url}/health', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Render middleware health check: {data}")
            return True
    except Exception as e:
        print(f"Render middleware not available: {e}")
    
    return False

def test_flutter_app():
    """Test Flutter app availability"""
    try:
        # Try localhost first
        response = requests.get('http://localhost:8080', timeout=5)
        if response.status_code == 200:
            print("✓ Local Flutter app is running")
            return True
    except Exception as e:
        print(f"Local Flutter app not available: {e}")
    
    # Try Render URL if available
    render_url = os.environ.get('RENDER_FLUTTER_URL', 'https://canteen-app.onrender.com')
    try:
        response = requests.get(render_url, timeout=10)
        if response.status_code == 200:
            print("✓ Render Flutter app is running")
            return True
    except Exception as e:
        print(f"Render Flutter app not available: {e}")
    
    return False

def test_api_endpoints():
    """Test middleware API endpoints"""
    base_url = 'http://localhost:5000'
    render_url = os.environ.get('RENDER_MIDDLEWARE_URL', 'https://canteen-middleware.onrender.com')
    
    # Test endpoints
    endpoints = [
        '/health',
        '/students/1/fees',
        '/test-print'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'{base_url}{endpoint}', timeout=5)
            print(f"✓ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint}: {e}")
            
            # Try Render URL
            try:
                response = requests.get(f'{render_url}{endpoint}', timeout=10)
                print(f"✓ {endpoint} (Render): {response.status_code}")
            except Exception as e2:
                print(f"✗ {endpoint} (Render): {e2}")

def main():
    print("Testing deployment...")
    print("=" * 50)
    
    # Test middleware
    print("Testing middleware...")
    middleware_ok = test_middleware_health()
    
    # Test Flutter app
    print("\nTesting Flutter app...")
    flutter_ok = test_flutter_app()
    
    # Test API endpoints
    print("\nTesting API endpoints...")
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    if middleware_ok and flutter_ok:
        print("✓ All tests passed! Deployment is working correctly.")
    else:
        print("✗ Some tests failed. Please check the deployment.")
    
    return middleware_ok and flutter_ok

if __name__ == "__main__":
    main()