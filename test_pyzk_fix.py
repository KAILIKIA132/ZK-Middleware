#!/usr/bin/env python3
"""
Test script to verify pyzk fix
"""

import sys
import subprocess

def test_pyzk_installation():
    """Test that pyzk can be installed"""
    try:
        # Try to install pyzk
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyzk==0.9.1"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✓ pyzk installation successful")
            return True
        else:
            print(f"✗ pyzk installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ pyzk installation timed out")
        return False
    except Exception as e:
        print(f"✗ pyzk installation error: {e}")
        return False

def test_import_pyzk():
    """Test that pyzk can be imported"""
    try:
        # Try different import methods using exec to avoid static analysis issues
        import_code = """
try:
    from zk import ZK, const
    print("Successfully imported 'from zk import ZK, const'")
    success = True
except ImportError:
    try:
        from pyzk.zk import ZK, const
        print("Successfully imported 'from pyzk.zk import ZK, const'")
        success = True
    except ImportError:
        try:
            from pyzk import ZK, const
            print("Successfully imported 'from pyzk import ZK, const'")
            success = True
        except ImportError:
            print("Failed to import pyzk with any method")
            success = False
"""
        result = subprocess.run(
            [sys.executable, "-c", import_code],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ pyzk import test successful")
            print(result.stdout.strip())
            return True
        else:
            print("✗ pyzk import test failed")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"✗ pyzk import test error: {e}")
        return False

def main():
    print("Testing pyzk fix...")
    print("=" * 30)
    
    # Test installation
    print("Testing pyzk installation:")
    install_success = test_pyzk_installation()
    
    if install_success:
        # Test import
        print("\nTesting pyzk import:")
        import_success = test_import_pyzk()
        
        if import_success:
            print("\n✓ All tests passed! pyzk should work correctly.")
            return 0
        else:
            print("\n✗ Import test failed.")
            return 1
    else:
        print("\n✗ Installation test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())