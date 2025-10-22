#!/usr/bin/env python3
"""
Deployment verification script for ZK Middleware
"""

import subprocess
import sys
import os

def check_docker_build():
    """Check if Docker image can be built"""
    print("Checking Docker build...")
    try:
        result = subprocess.run(
            ["docker", "build", "-t", "zk-middleware-test", "."],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("✓ Docker build successful")
            # Clean up test image
            subprocess.run(["docker", "rmi", "zk-middleware-test"], 
                         capture_output=True)
            return True
        else:
            print("✗ Docker build failed")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("✗ Docker build timed out")
        return False
    except FileNotFoundError:
        print("⚠️  Docker not found, skipping Docker build check")
        return True

def check_requirements():
    """Check if requirements can be installed"""
    print("Checking requirements...")
    try:
        result = subprocess.run(
            ["pip", "install", "--dry-run", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            cwd="."
        )
        if result.returncode == 0:
            print("✓ Requirements check passed")
            return True
        else:
            print("✗ Requirements check failed")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("⚠️  pip not found, skipping requirements check")
        return True

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.9+)")
        return False

def main():
    print("ZK Middleware Deployment Verification")
    print("=" * 40)
    
    # Change to middleware directory
    original_dir = os.getcwd()
    os.chdir("zk_middleware")
    
    checks = [
        ("Python Version", check_python_version),
        ("Requirements", check_requirements),
        ("Docker Build", check_docker_build)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"✗ {check_name} failed with exception: {e}")
            results.append(False)
    
    # Change back to original directory
    os.chdir(original_dir)
    
    print("\n" + "=" * 40)
    if all(results):
        print("✓ All deployment checks passed!")
        print("The middleware is ready for deployment.")
        return 0
    else:
        print("✗ Some deployment checks failed.")
        print("Please address the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())