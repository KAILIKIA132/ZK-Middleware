from escpos.printer import Network, Usb, File
import logging
import time

logger = logging.getLogger(__name__)

class TicketPrinter:
    def __init__(self, cfg):
        self.cfg = cfg
        self.printer = None
        self._connect()

    def _connect(self):
        try:
            if self.cfg.get("type") == "network":
                host = self.cfg["network"]["host"]
                port = self.cfg["network"].get("port", 9100)
                self.printer = Network(host, port=port, timeout=5)
            elif self.cfg.get("type") == "usb":
                # adjust ids for your printer
                self.printer = Usb(0x04b8, 0x0202)
            else:
                # fallback to file
                self.printer = File('/dev/usb/lp0')
        except Exception as e:
            logger.exception("Printer connection failed: %s", e)
            self.printer = None

    def print_ticket(self, student_name, student_id, details):
        if not self.printer:
            logger.error("No printer available")
            return False
        try:
            p = self.printer
            p.set(align='center', width=2, height=2)
            p.text("CRAWFORD INTERNATIONAL\n")
            p.text("CAFETERIA\n")
            p.set(align='left', width=1, height=1)
            p.text("------------------------------\n")
            p.text(f"Student: {student_name}\n")
            p.text(f"ID: {student_id}\n")
            p.text(f"{details}\n")
            p.text(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            p.text("------------------------------\n")
            p.text("Thank you. Enjoy your meal!\n")
            p.cut()
            return True
        except Exception as e:
            logger.exception("Printing failed: %s", e)
            return False

    def print_error(self, message):
        if not self.printer:
            logger.error("No printer available")
            return False
        try:
            p = self.printer
            p.set(align='center', width=2, height=2)
            p.text("ACCESS DENIED\n")
            p.set(align='left', width=1, height=1)
            p.text("------------------------------\n")
            p.text(f"{message}\n")
            p.text("------------------------------\n")
            p.text("Please contact administration.\n")
            p.cut()
            return True
        except Exception as e:
            logger.exception("Printing error failed: %s", e)
            return False