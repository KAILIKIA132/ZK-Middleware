#!/usr/bin/env python3
"""
Test script to verify middleware build
"""

import subprocess
import sys
import os

def test_docker_build():
    """Test Docker build for middleware"""
    print("Testing Docker build for middleware...")
    
    try:
        # Change to middleware directory
        os.chdir("zk_middleware")
        
        # Run docker build
        result = subprocess.run(
            ["docker", "build", "-t", "zk-middleware-test", "."],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✓ Docker build successful!")
            print(result.stdout)
            return True
        else:
            print("✗ Docker build failed!")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Docker build timed out!")
        return False
    except Exception as e:
        print(f"✗ Docker build error: {e}")
        return False
    finally:
        # Change back to parent directory
        os.chdir("..")

def main():
    print("Testing middleware build...")
    print("=" * 40)
    
    success = test_docker_build()
    
    print("=" * 40)
    if success:
        print("✓ All tests passed! Middleware is ready for deployment.")
    else:
        print("✗ Tests failed! Please check the build configuration.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())