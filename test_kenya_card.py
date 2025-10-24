#!/usr/bin/env python3
"""
Test script for the Kenya-themed meal card printing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from printer import TicketPrinter
import yaml

def test_kenya_meal_card():
    """Test the Kenya-themed meal card printing"""
    
    # Create a mock printer configuration
    mock_config = {
        "type": "file",
        "file": "/tmp/test_meal_card.txt"
    }
    
    # Initialize printer with file output for testing
    printer = TicketPrinter(mock_config)
    
    if not printer.printer:
        print("❌ Failed to initialize printer")
        return False
    
    print("Testing Kenya-themed meal card printing...")
    
    # Test successful meal card
    print("\n1. Testing successful meal card:")
    success = printer.print_ticket(
        student_name="Wangari Maathai",
        student_id="1001",
        details="Lunch - KES 150.00"
    )
    
    if success:
        print("✅ Meal card printed successfully")
        # Display the content
        try:
            with open("/tmp/test_meal_card.txt", "r") as f:
                content = f.read()
                print("📄 Generated card content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❌ Error reading test file: {e}")
    else:
        print("❌ Failed to print meal card")
        return False
    
    # Test error card
    print("\n2. Testing error card:")
    error_success = printer.print_error(
        message="Fee not paid for today's meal"
    )
    
    if error_success:
        print("✅ Error card printed successfully")
        # Display the content
        try:
            with open("/tmp/test_meal_card.txt", "r") as f:
                content = f.read()
                print("📄 Generated error card content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❌ Error reading test file: {e}")
    else:
        print("❌ Failed to print error card")
        return False
    
    print("\n🎉 All Kenya-themed card tests completed!")
    return True

def create_file_printer_config():
    """Create a configuration for file-based printing for testing"""
    config = {
        "type": "file",
        "file": "/tmp/test_meal_card.txt"
    }
    return config

if __name__ == "__main__":
    print("Kenya-Themed Meal Card Testing")
    print("=" * 40)
    
    # Test with file-based printer for development
    test_kenya_meal_card()