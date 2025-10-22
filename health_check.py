#!/usr/bin/env python3
"""
Health check script for ZK Middleware
"""

import requests
import sys
import os

def check_health():
    """Check if the middleware is healthy"""
    port = os.environ.get("PORT", "5000")
    url = f"http://localhost:{port}/health"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("✓ Middleware is healthy")
                return True
            else:
                print(f"✗ Middleware returned unexpected status: {data}")
                return False
        else:
            print(f"✗ Middleware returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to middleware. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("✗ Health check timed out")
        return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def main():
    print("Checking ZK Middleware health...")
    print("=" * 35)
    
    success = check_health()
    
    print("=" * 35)
    if success:
        print("✓ Health check passed!")
        return 0
    else:
        print("✗ Health check failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())