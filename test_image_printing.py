#!/usr/bin/env python3
"""
Test script for image printing on meal cards
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from printer import TicketPrinter
import time

def test_image_printing():
    """Test meal card printing with student images"""
    
    # Create a file-based printer for testing
    config = {
        "type": "file",
        "file": "/tmp/image_test_card.txt"
    }
    
    printer = TicketPrinter(config)
    
    if not printer.printer:
        print("❌ Failed to initialize printer")
        return False
    
    print("Testing meal card printing with student image...")
    
    # Test success card with image
    print("\n1. Testing success card with student image:")
    success = printer.print_ticket(
        student_name="Wangari Maathai",
        student_id="1001",
        details="Lunch - KES 150.00",
        photo_url="https://placehold.co/100x100/4a90e2/ffffff?text=WM"
    )
    
    if success:
        print("✅ Success card with image printed successfully")
        # Display the content
        try:
            with open("/tmp/image_test_card.txt", "r") as f:
                content = f.read()
                print("📄 Generated card content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❌ Error reading test file: {e}")
    else:
        print("❌ Failed to print success card with image")
        return False
    
    # Test error card with image
    print("\n2. Testing error card with student image:")
    error_success = printer.print_error(
        message="Fee not paid for today's meal",
        photo_url="https://placehold.co/100x100/e74c3c/ffffff?text=JK"
    )
    
    if error_success:
        print("✅ Error card with image printed successfully")
        # Display the content
        try:
            with open("/tmp/image_test_card.txt", "r") as f:
                content = f.read()
                print("📄 Generated error card content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❌ Error reading test file: {e}")
    else:
        print("❌ Failed to print error card with image")
        return False
    
    print("\n🎉 All image printing tests completed!")
    return True

if __name__ == "__main__":
    print("Kenya-Themed Meal Card with Image Printing Test")
    print("=" * 50)
    
    test_image_printing()