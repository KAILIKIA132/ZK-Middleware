import logging
import threading
import time
from flask import Flask, request, jsonify, render_template
import yaml
import requests
from zk_device import ZKDevice
from printer import TicketPrinter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("zk-middleware")

# Load config
with open("config.example.yml", "r") as f:
    cfg = yaml.safe_load(f)

device_cfg = cfg["device"]
api_cfg = cfg["school_api"]
printer_cfg = cfg.get("printer", {})

zk = ZKDevice(device_cfg["ip"], port=device_cfg.get("port", 4370), timeout=device_cfg.get("timeout", 10))
printer = TicketPrinter(printer_cfg)

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
            # Print ticket
            ok = printer.print_ticket(student_name=name, student_id=student_id, details=details)
            if ok:
                logger.info("Ticket printed for %s", student_id)
                # optionally send device display success
                zk.send_display_message("Access granted - Ticket printed")
        else:
            # send error to device and log
            reason = res.get("error", "Unpaid")
            zk.send_display_message("Fee unpaid. Contact admin.")
            printer.print_error("Fee not paid for today's meal")
            logger.info("Student %s not paid: %s", student_id, reason)
    except Exception as e:
        logger.exception("Error processing log: %s", e)

def polling_loop(poll_interval=5):
    logger.info("Starting device polling loop")
    while True:
        try:
            logs = zk.pull_attendance()
            if logs:
                for l in logs:
                    handle_log_entry(l)
            time.sleep(poll_interval)
        except Exception as e:
            logger.exception("Polling loop error: %s. Reconnecting...", e)
            zk.disconnect()
            time.sleep(5)
            zk.connect()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/test-print", methods=["POST"])
def test_print():
    payload = request.json or {}
    student_name = payload.get("name", "Test Student")
    student_id = payload.get("id", "000")
    details = payload.get("details", "Test printing")
    ok = printer.print_ticket(student_name, student_id, details)
    return jsonify({"printed": ok})

@app.route("/test-error", methods=["POST"])
def test_error():
    payload = request.json or {}
    message = payload.get("message", "Test error message")
    ok = printer.print_error(message)
    return jsonify({"printed": ok})

@app.route("/admin", methods=["GET"])
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    # Connect device before starting
    zk.connect()
    # Start polling in background thread
    t = threading.Thread(target=polling_loop, args=(3,), daemon=True)
    t.start()
    app.run(host=cfg["app"]["listen_host"], port=cfg["app"]["listen_port"])