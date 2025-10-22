#!/usr/bin/env python3
"""
Script to fix common deployment issues
"""

import os
import re

def fix_requirements():
    """Fix requirements.txt for Render deployment"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"Requirements file {requirements_file} not found!")
        return False
    
    try:
        with open(requirements_file, "r") as f:
            content = f.read()
        
        # Fix gunicorn version
        content = re.sub(r"gunicorn==22\.1\.0", "gunicorn==22.0.0", content)
        
        with open(requirements_file, "w") as f:
            f.write(content)
        
        print("✓ Fixed requirements.txt")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing requirements.txt: {e}")
        return False

def check_dockerfile():
    """Check Dockerfile for common issues"""
    dockerfile = "Dockerfile"
    
    if not os.path.exists(dockerfile):
        print(f"Dockerfile {dockerfile} not found!")
        return False
    
    try:
        with open(dockerfile, "r") as f:
            content = f.read()
        
        # Check if pip upgrade is present
        if "pip install --upgrade pip" not in content:
            print("⚠️  Consider adding 'RUN pip install --upgrade pip' to Dockerfile")
        
        # Check if PORT is used correctly
        if "PORT" not in content and "5000" not in content:
            print("⚠️  Check that Dockerfile exposes the correct port")
        
        print("✓ Dockerfile check completed")
        return True
        
    except Exception as e:
        print(f"✗ Error checking Dockerfile: {e}")
        return False

def main():
    print("Fixing common deployment issues...")
    print("=" * 40)
    
    os.chdir("zk_middleware")
    
    success1 = fix_requirements()
    success2 = check_dockerfile()
    
    print("=" * 40)
    if success1 and success2:
        print("✓ All fixes applied successfully!")
    else:
        print("⚠️  Some issues may still need attention")
    
    return 0

if __name__ == "__main__":
    main()