#!/usr/bin/env python3
"""
Check if all requirements can be installed
"""

import subprocess
import sys

def check_requirements():
    """Check if requirements can be installed"""
    print("Checking requirements...")
    
    try:
        # Run pip check
        result = subprocess.run(
            ["pip", "install", "--dry-run", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            cwd="zk_middleware"
        )
        
        if result.returncode == 0:
            print("✓ All requirements can be installed!")
            return True
        else:
            print("✗ Requirements check failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error checking requirements: {e}")
        return False

def main():
    print("Checking middleware requirements...")
    print("=" * 40)
    
    success = check_requirements()
    
    print("=" * 40)
    if success:
        print("✓ Requirements check passed!")
    else:
        print("✗ Requirements check failed!")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())