#!/usr/bin/env python3
"""
Test script for school management system API integration
"""

import requests
import json

# Test configuration
BASE_URL = "https://school.example.com/api"
API_KEY = "test_api_key"

def test_payment_status(student_id):
    """Test checking payment status for a student"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}/students/{student_id}/fees"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_mock_server():
    """Create a simple mock server for testing"""
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route("/api/students/<student_id>/fees", methods=["GET"])
    def get_payment_status(student_id):
        # Mock data for testing
        mock_data = {
            "1001": {"paid": True, "details": "Lunch payment confirmed"},
            "1002": {"paid": False, "details": "Lunch payment not found"},
            "1003": {"paid": True, "details": "Lunch payment confirmed"}
        }
        
        if student_id in mock_data:
            return jsonify(mock_data[student_id])
        else:
            return jsonify({"paid": False, "details": "Student not found"}), 404
    
    app.run(port=8080, debug=True)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "mock":
        print("Starting mock server on port 8080...")
        test_mock_server()
    else:
        print("Testing API with student ID 1001...")
        test_payment_status("1001")