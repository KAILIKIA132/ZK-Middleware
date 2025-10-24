import logging
import threading
import time
import os
from flask import Flask, request, jsonify, render_template
import yaml
import requests
# Import our device and printer modules with error handling
try:
    from zk_device import ZKDevice
    from printer import TicketPrinter
except ImportError as e:
    logging.warning("Failed to import device/printer modules: %s", e)
    ZKDevice = None
    TicketPrinter = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zk-middleware")

# Load config from environment variables or config file
device_ip = os.environ.get("DEVICE_IP", "192.168.1.100")
device_port = int(os.environ.get("DEVICE_PORT", "4370"))
device_timeout = int(os.environ.get("DEVICE_TIMEOUT", "10"))

school_api_base_url = os.environ.get("SCHOOL_API_BASE_URL", "https://school.example.com/api")
school_api_key = os.environ.get("SCHOOL_API_KEY", "REPLACE_WITH_SECRET")

printer_type = os.environ.get("PRINTER_TYPE", "network")
printer_host = os.environ.get("PRINTER_HOST", "192.168.1.200")
printer_port = int(os.environ.get("PRINTER_PORT", "9100"))

listen_host = os.environ.get("LISTEN_HOST", "0.0.0.0")
listen_port = int(os.environ.get("PORT", "5000"))

# Create config dictionary
# Handle file-based printer configuration
if printer_type == "file":
    printer_file = os.environ.get("PRINTER_FILE", "/tmp/meal_card.txt")
    printer_config = {
        "type": printer_type,
        "file": printer_file
    }
else:
    printer_config = {
        "type": printer_type,
        "network": {
            "host": printer_host,
            "port": printer_port
        }
    }

cfg = {
    "device": {
        "ip": device_ip,
        "port": device_port,
        "timeout": device_timeout
    },
    "school_api": {
        "base_url": school_api_base_url,
        "api_key": school_api_key
    },
    "printer": printer_config,
    "app": {
        "listen_host": listen_host,
        "listen_port": listen_port
    }
}

# Initialize services with error handling
device_cfg = cfg["device"]
api_cfg = cfg["school_api"]
printer_cfg = cfg.get("printer", {})

# Global variables for services
zk = None
printer = None

def init_services():
    """Initialize services lazily to avoid issues with worker processes"""
    global zk, printer
    if zk is None and ZKDevice is not None:
        try:
            zk = ZKDevice(device_cfg["ip"], port=device_cfg.get("port", 4370), timeout=device_cfg.get("timeout", 10))
        except Exception as e:
            logger.error("Failed to initialize ZKDevice: %s", e)
            zk = None
    if printer is None and TicketPrinter is not None:
        try:
            printer = TicketPrinter(printer_cfg)
        except Exception as e:
            logger.error("Failed to initialize TicketPrinter: %s", e)
            printer = None

app = Flask(__name__, template_folder='templates')

# In-memory seen logs to avoid duplicates (simple approach)
seen_log_ids = set()

def check_payment(student_id):
    """
    Query the school system to check paid status.
    Expecting endpoint: GET /api/students/{id}/fees
    returns JSON { "paid": true, "details": "..." }
    """
    headers = {"Authorization": f"Bearer {api_cfg.get('api_key', '')}"}
    url = f"{api_cfg['base_url'].rstrip('/')}/students/{student_id}/fees"
    try:
        r = requests.get(url, headers=headers, timeout=6, verify=True)
        if r.status_code == 200:
            return r.json()
        else:
            logger.warning("School API returned %s for %s", r.status_code, student_id)
            return {"paid": False, "error": "api_error"}
    except Exception as e:
        logger.exception("School API call failed: %s", e)
        return {"paid": False, "error": "exception"}

def handle_log_entry(log):
    """
    Process a single attendance/log entry.
    log format depends on pyzk/device. Commonly:
    (uid, timestamp, status, punch)
    or object with attributes.
    We'll be defensive when parsing.
    """
    # Initialize services if not already done
    init_services()
    
    # Example parsing - adapt to actual log structure
    try:
        # pyzk returns object with user_id or tuple. Try both
        if hasattr(log, 'user_id'):
            student_id = str(log.user_id)
            event_id = getattr(log, 'id', f"{student_id}-{log.timestamp}")
            name = getattr(log, 'name', 'Unknown')
        else:
            # tuple: (uid, timestamp, status)
            student_id = str(log[0])
            event_id = f"{student_id}-{str(log[1])}"
            name = "Unknown"

        if event_id in seen_log_ids:
            return
        seen_log_ids.add(event_id)

        logger.info("Processing log for student_id=%s event=%s", student_id, event_id)

        # Call school API
        res = check_payment(student_id)
        if res.get("paid"):
            details = res.get("details", "Lunch payment confirmed")
            # Print ticket with student photo
            if printer is not None:
                photo_url = res.get("photo_url")
                ok = printer.print_ticket(student_name=name, student_id=student_id, details=details, photo_url=photo_url)
                if ok:
                    logger.info("Ticket printed for %s", student_id)
                    # optionally send device display success
                    if zk is not None:
                        zk.send_display_message("Access granted - Ticket printed")
                else:
                    logger.warning("Failed to print ticket for %s", student_id)
            else:
                logger.warning("Printer not available, skipping ticket print for %s", student_id)
        else:
            # send error to device and log
            reason = res.get("error", "Unpaid")
            if zk is not None:
                zk.send_display_message("Fee unpaid. Contact admin.")
            if printer is not None:
                photo_url = res.get("photo_url")
                printer.print_error("Fee not paid for today's meal", photo_url=photo_url)
            logger.info("Student %s not paid: %s", student_id, reason)
    except Exception as e:
        logger.exception("Error processing log: %s", e)

def polling_loop(poll_interval=5):
    """Polling loop for device attendance logs"""
    # Initialize services
    init_services()
    
    # Skip polling if ZK device is not available
    if zk is None:
        logger.warning("ZK device not available, skipping polling loop")
        return
        
    logger.info("Starting device polling loop")
    while True:
        try:
            # Connect to device if not already connected
            if not hasattr(zk, '_connected') or not zk._connected:
                zk.connect()
                zk._connected = True
                
            logs = zk.pull_attendance()
            if logs:
                for l in logs:
                    handle_log_entry(l)
            time.sleep(poll_interval)
        except Exception as e:
            logger.exception("Polling loop error: %s. Reconnecting...", e)
            try:
                zk.disconnect()
                zk._connected = False
            except:
                pass
            time.sleep(5)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/test-print", methods=["POST"])
def test_print():
    # Initialize services if not already done
    init_services()
    
    if printer is None:
        return jsonify({"printed": False, "error": "Printer not available"}), 500
    
    payload = request.json or {}
    student_name = payload.get("name", "Test Student")
    student_id = payload.get("id", "000")
    details = payload.get("details", "Test printing")
    ok = printer.print_ticket(student_name, student_id, details)
    return jsonify({"printed": ok})

@app.route("/test-error", methods=["POST"])
def test_error():
    # Initialize services if not already done
    init_services()
    
    if printer is None:
        return jsonify({"printed": False, "error": "Printer not available"}), 500
    
    payload = request.json or {}
    message = payload.get("message", "Test error message")
    photo_url = payload.get("photo_url")
    ok = printer.print_error(message, photo_url=photo_url)
    return jsonify({"printed": ok})

@app.route("/admin", methods=["GET"])
def admin():
    # Prepare dynamic data for the admin template
    
    # Initialize services to check their status
    init_services()
    
    # System status data
    middleware_status = "running"
    device_status = "connected" if zk and hasattr(zk, '_connected') and zk._connected else "disconnected"
    printer_status = "ready" if printer and printer.printer else "not available"
    
    # Device information
    device_model = "SpeedFace M4 (Simulated)"
    device_ip = cfg.get("device", {}).get("ip", "192.168.1.100")
    device_connection_status = "Active" if device_status == "connected" else "Inactive"
    
    # Recent activity (in a real implementation, this would come from a database or log)
    recent_activity = [
        {"timestamp": "2025-10-24 14:30", "student_name": "Wangari Maathai", "status": "Access Granted"},
        {"timestamp": "2025-10-24 14:25", "student_name": "Jomo Kenyatta", "status": "Access Denied (Unpaid)"},
        {"timestamp": "2025-10-24 14:20", "student_name": "Chinua Achebe", "status": "Access Granted"}
    ]
    
    # System logs (in a real implementation, this would come from actual logs)
    system_logs = [
        "[INFO] Middleware started successfully",
        "[INFO] Attempting to connect to ZK device 192.168.1.100:4370",
        "[WARNING] Failed to connect to ZK device: can't reach device (ping 192.168.1.100)",
        "[INFO] Printer initialization completed",
        "[INFO] Mock school API connection established"
    ]
    
    return render_template('admin.html', 
                         middleware_status=middleware_status,
                         device_status=device_status,
                         printer_status=printer_status,
                         device_model=device_model,
                         device_ip=device_ip,
                         device_connection_status=device_connection_status,
                         recent_activity=recent_activity,
                         system_logs=system_logs)

@app.route("/students/<student_id>/fees", methods=["GET"])
def student_fees(student_id):
    """
    Endpoint for checking student payment status
    """
    try:
        # Call the school API to check payment status
        result = check_payment(student_id)
        
        if "error" in result:
            return jsonify(result), 500
        else:
            return jsonify(result)
    except Exception as e:
        logger.exception("Error checking student fees: %s", e)
        return jsonify({"paid": False, "details": "Internal server error"}), 500

@app.route("/attendance", methods=["POST"])
def log_attendance():
    """
    Endpoint for logging attendance
    """
    try:
        data = request.json or {}
        student_id = data.get("student_id")
        timestamp = data.get("timestamp")
        device_id = data.get("device_id", "unknown")
        
        if not student_id:
            return jsonify({"error": "student_id is required"}), 400
            
        logger.info("Attendance logged for student %s at %s from device %s", 
                   student_id, timestamp, device_id)
        
        return jsonify({"message": "Attendance logged successfully"}), 201
    except Exception as e:
        logger.exception("Error logging attendance: %s", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/print-ticket", methods=["POST"])
def print_ticket():
    """
    Endpoint for printing tickets
    """
    # Initialize services if not already done
    init_services()
    
    if printer is None:
        return jsonify({"error": "Printer not available"}), 500
    
    try:
        data = request.json or {}
        student_id = data.get("student_id")
        student_name = data.get("student_name", "Unknown Student")
        meal_type = data.get("meal_type", "Lunch")
        amount = data.get("amount", 0.0)
        timestamp = data.get("timestamp")
        photo_url = data.get("photo_url")
        
        if not student_id:
            return jsonify({"error": "student_id is required"}), 400
            
        details = f"{meal_type} - R{amount:.2f}"
        ok = printer.print_ticket(student_name, student_id, details, photo_url=photo_url)
        
        if ok:
            return jsonify({"message": "Ticket printed successfully"}), 200
        else:
            return jsonify({"error": "Failed to print ticket"}), 500
    except Exception as e:
        logger.exception("Error printing ticket: %s", e)
        return jsonify({"error": "Internal server error"}), 500

def start_polling():
    """Start the polling loop in a separate thread"""
    # Only start polling in one worker process
    if os.environ.get("POLLING_STARTED") != "true":
        os.environ["POLLING_STARTED"] = "true"
        polling_thread = threading.Thread(target=polling_loop, args=(3,), daemon=True)
        polling_thread.start()
        logger.info("Polling thread started")

if __name__ == "__main__":
    # Initialize services
    init_services()
    
    # Start polling in background thread (only in main process)
    start_polling()
    
    # Run the Flask app
    app.run(host=cfg["app"]["listen_host"], port=cfg["app"]["listen_port"])