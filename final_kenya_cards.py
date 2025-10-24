#!/usr/bin/env python3
"""
Generate final Kenya-themed meal card samples
"""

from printer import TicketPrinter

def generate_sample_cards():
    """Generate sample cards for documentation"""
    
    # Success card
    success_config = {'type': 'file', 'file': '/tmp/kenya_success_card.txt'}
    success_printer = TicketPrinter(success_config)
    
    if success_printer.printer:
        success_printer.print_ticket(
            student_name="Wangari Maathai", 
            student_id="1001", 
            details="Lunch - KES 150.00"
        )
    
    # Error card
    error_config = {'type': 'file', 'file': '/tmp/kenya_error_card.txt'}
    error_printer = TicketPrinter(error_config)
    
    if error_printer.printer:
        error_printer.print_error(
            message="Fee not paid for today's meal"
        )
    
    print("Kenya-Themed Meal Card Samples Generated")
    print("=" * 40)
    print("Files created:")
    print("  /tmp/kenya_success_card.txt")
    print("  /tmp/kenya_error_card.txt")
    
    # Display success card
    print("\nSUCCESS MEAL CARD:")
    print("=" * 50)
    try:
        with open('/tmp/kenya_success_card.txt', 'r') as f:
            content = f.read()
            # Clean up any special characters
            clean_content = content.replace('\x00', '').replace('\x1b', '').replace('\x1d', '')
            print(clean_content)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    print("=" * 50)
    
    # Display error card
    print("\nERROR MEAL CARD:")
    print("=" * 50)
    try:
        with open('/tmp/kenya_error_card.txt', 'r') as f:
            content = f.read()
            # Clean up any special characters
            clean_content = content.replace('\x00', '').replace('\x1b', '').replace('\x1d', '')
            print(clean_content)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    generate_sample_cards()