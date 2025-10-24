#!/usr/bin/env python3
"""
Test script for JPEG image printing on meal cards
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from printer import TicketPrinter

def test_jpeg_image_printing():
    """Test meal card printing with JPEG student images"""
    
    # Create a file-based printer for testing
    config = {
        "type": "file",
        "file": "/tmp/jpeg_test_card.txt"
    }
    
    printer = TicketPrinter(config)
    
    if not printer.printer:
        print("❌ Failed to initialize printer")
        return False
    
    print("Testing meal card printing with JPEG student image...")
    
    # Test success card with JPEG image
    print("\n1. Testing success card with JPEG image:")
    success = printer.print_ticket(
        student_name="Wangari Maathai",
        student_id="1001",
        details="Lunch - KES 150.00",
        photo_url="https://picsum.photos/100/100"  # This provides a JPEG image
    )
    
    if success:
        print("✅ Success card with JPEG image printed successfully")
        # Display the content
        try:
            with open("/tmp/jpeg_test_card.txt", "r") as f:
                content = f.read()
                print("📄 Generated card content:")
                print("-" * 40)
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❌ Error reading test file: {e}")
    else:
        print("❌ Failed to print success card with JPEG image")
        return False
    
    print("\n🎉 JPEG image printing test completed!")
    return True

if __name__ == "__main__":
    print("Kenya-Themed Meal Card with JPEG Image Printing Test")
    print("=" * 50)
    
    test_jpeg_image_printing()