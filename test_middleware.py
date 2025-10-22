#!/usr/bin/env python3
"""
Test script for the ZK Middleware components
"""

import yaml
from zk_device import ZKDevice
from printer import TicketPrinter

def test_config_loading():
    """Test loading configuration"""
    try:
        with open("config.example.yml", "r") as f:
            cfg = yaml.safe_load(f)
        print("✓ Configuration loaded successfully")
        return cfg
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return None

def test_device_connection(cfg):
    """Test connection to ZK device"""
    if not cfg:
        return False
        
    try:
        device_cfg = cfg["device"]
        zk = ZKDevice(
            device_cfg["ip"], 
            port=device_cfg.get("port", 4370), 
            timeout=device_cfg.get("timeout", 10)
        )
        result = zk.connect()
        if result:
            print("✓ Connected to ZK device")
            # Test getting users
            users = zk.get_users()
            print(f"  Found {len(users)} users in device")
            zk.disconnect()
            return True
        else:
            print("✗ Failed to connect to ZK device")
            return False
    except Exception as e:
        print(f"✗ Error testing device connection: {e}")
        return False

def test_printer_connection(cfg):
    """Test connection to printer"""
    if not cfg:
        return False
        
    try:
        printer_cfg = cfg.get("printer", {})
        printer = TicketPrinter(printer_cfg)
        if printer.printer:
            print("✓ Connected to printer")
            return True
        else:
            print("✗ Failed to connect to printer")
            return False
    except Exception as e:
        print(f"✗ Error testing printer connection: {e}")
        return False

def main():
    print("Testing ZK Middleware Components")
    print("=" * 40)
    
    # Test configuration
    cfg = test_config_loading()
    
    # Test device connection
    test_device_connection(cfg)
    
    # Test printer connection
    test_printer_connection(cfg)
    
    print("=" * 40)
    print("Testing completed")

if __name__ == "__main__":
    main()