#!/usr/bin/env python3
"""
Mock server for school management system API
Simulates Kenyan student information and fee payment status
"""

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Mock data for Kenyan students
mock_student_data = {
    "1001": {
        "student_id": "1001",
        "name": "Wangari Maathai",
        "grade": "Grade 8",
        "class": "8A",
        "paid": True,
        "details": "Lunch payment confirmed",
        "amount": 150.00,
        "balance": 0.00,
        "last_payment_date": "2025-10-20",
        "photo_url": "https://placehold.co/100x100/4a90e2/ffffff?text=WM"
    },
    "1002": {
        "student_id": "1002",
        "name": "Jomo Kenyatta",
        "grade": "Grade 7",
        "class": "7B",
        "paid": False,
        "details": "Lunch payment not found",
        "amount": 150.00,
        "balance": 150.00,
        "last_payment_date": None,
        "photo_url": "https://placehold.co/100x100/e74c3c/ffffff?text=JK"
    },
    "1003": {
        "student_id": "1003",
        "name": "Chinua Achebe",
        "grade": "Grade 9",
        "class": "9C",
        "paid": True,
        "details": "Lunch payment confirmed",
        "amount": 150.00,
        "balance": 0.00,
        "last_payment_date": "2025-10-22",
        "photo_url": "https://placehold.co/100x100/27ae60/ffffff?text=CA"
    },
    "1004": {
        "student_id": "1004",
        "name": "Grace Ogot",
        "grade": "Grade 6",
        "class": "6A",
        "paid": True,
        "details": "Lunch payment confirmed",
        "amount": 150.00,
        "balance": 0.00,
        "last_payment_date": "2025-10-18",
        "photo_url": "https://placehold.co/100x100/f39c12/ffffff?text=GO"
    },
    "1005": {
        "student_id": "1005",
        "name": "Ngugi wa Thiong'o",
        "grade": "Grade 10",
        "class": "10B",
        "paid": False,
        "details": "Lunch payment not found",
        "amount": 150.00,
        "balance": 150.00,
        "last_payment_date": None,
        "photo_url": "https://placehold.co/100x100/8e44ad/ffffff?text=NW"
    }
}

@app.route("/api/students/<student_id>/fees", methods=["GET"])
def get_student_fees(student_id):
    """Get fee payment status for a student"""
    # Check if API key is provided
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401
    
    api_key = auth_header.split(' ')[1]
    # In a real implementation, you would validate the API key
    # For this mock, we'll accept any key
    
    if student_id in mock_student_data:
        return jsonify(mock_student_data[student_id])
    else:
        return jsonify({
            "student_id": student_id,
            "paid": False,
            "details": "Student not found",
            "amount": 0.00,
            "balance": 0.00
        }), 404

@app.route("/api/students", methods=["GET"])
def get_all_students():
    """Get all students (simplified list)"""
    students_list = [
        {"student_id": sid, "name": data["name"], "grade": data["grade"], "paid": data["paid"]}
        for sid, data in mock_student_data.items()
    ]
    return jsonify(students_list)

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "School Management API Mock"})

if __name__ == "__main__":
    print("Starting mock school API server...")
    print("Endpoints available:")
    print("  GET /api/health")
    print("  GET /api/students")
    print("  GET /api/students/<student_id>/fees")
    print("Server running on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)