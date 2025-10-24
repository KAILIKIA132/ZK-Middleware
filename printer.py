from escpos.printer import Network, Usb, File
import logging
import time
import requests
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    Image = None
    logging.warning("PIL not available, image printing will be disabled")

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
                self.printer = Usb(idVendor='0x04b8', idProduct='0x0202', timeout=5)
            else:
                # fallback to file - use configurable file path or default
                file_path = self.cfg.get("file", "/tmp/meal_card.txt")
                self.printer = File(file_path)
        except Exception as e:
            logger.exception("Printer connection failed: %s", e)
            self.printer = None

    def print_ticket(self, student_name, student_id, details, photo_url=None):
        if not self.printer:
            logger.error("No printer available")
            return False
        try:
            p = self.printer
            
            # Set up the professional Kenya-themed meal card
            
            # Header with Kenya colors
            p.set(align='center', width=2, height=2)
            p.text("KENYA SCHOOL MEAL PROGRAM\n")
            p.set(align='center', width=1, height=1)
            p.text("Ministry of Education\n")
            p.text("------------------------------\n")
            
            # Main title
            p.set(align='center', width=1, height=1)
            p.text("SCHOOL MEAL CARD\n")
            p.text("==============================\n\n")
            
            # Print student photo if available and PIL is installed
            if photo_url and Image:
                try:
                    response = requests.get(photo_url, timeout=5)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        # Resize image to fit on receipt (about 100x100 pixels)
                        image = image.resize((100, 100))
                        p.image(image, center=True)
                        p.text("\n")
                except Exception as e:
                    logger.warning("Failed to print student photo: %s", e)
            
            # Student information section
            p.set(align='left', width=1, height=1)
            p.text(f"Student Name: {student_name}\n")
            p.text(f"Student ID:   {student_id}\n")
            p.text(f"Meal Type:    {details}\n")
            p.text(f"Date:         {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Status section
            p.set(align='center', width=1, height=1)
            p.text("STATUS: AUTHORIZED\n")
            p.text("✔ MEAL APPROVED\n\n")
            
            # Motivational message
            p.set(align='center', width=1, height=1)
            p.text("""\n"Education is the most powerful weapon
which you can use to change the world."
- Nelson Mandela\n""")
            
            # Footer
            p.text("\n==============================\n")
            p.text("Enjoy your nutritious meal!\n")
            p.text("Harambee! (Pull together)\n")
            
            # Cut the ticket
            p.cut()
            return True
        except Exception as e:
            logger.exception("Printing failed: %s", e)
            return False

    def print_error(self, message, photo_url=None):
        if not self.printer:
            logger.error("No printer available")
            return False
        try:
            p = self.printer
            
            # Set up the professional Kenya-themed error card
            
            # Header with Kenya colors
            p.set(align='center', width=2, height=2)
            p.text("KENYA SCHOOL MEAL PROGRAM\n")
            p.set(align='center', width=1, height=1)
            p.text("Ministry of Education\n")
            p.text("------------------------------\n")
            
            # Main title
            p.set(align='center', width=1, height=1)
            p.text("MEAL CARD - ACCESS DENIED\n")
            p.text("==============================\n\n")
            
            # Print student photo if available and PIL is installed
            if photo_url and Image:
                try:
                    response = requests.get(photo_url, timeout=5)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        # Resize image to fit on receipt (about 100x100 pixels)
                        image = image.resize((100, 100))
                        p.image(image, center=True)
                        p.text("\n")
                except Exception as e:
                    logger.warning("Failed to print student photo: %s", e)
            
            # Error message
            p.set(align='center', width=1, height=1)
            p.text("❌ ACCESS DENIED\n")
            p.text(f"{message}\n\n")
            
            # Instructions
            p.text("Please contact the school\n")
            p.text("administration office to\n")
            p.text("resolve this issue.\n\n")
            
            # Motivational message
            p.set(align='center', width=1, height=1)
            p.text("""\n"The future belongs to those\nwho believe in the beauty\nof their dreams."
- Eleanor Roosevelt\n""")
            
            # Footer
            p.text("\n==============================\n")
            p.text("Harambee! (Pull together)\n")
            
            # Cut the ticket
            p.cut()
            return True
        except Exception as e:
            logger.exception("Printing error failed: %s", e)
            return False