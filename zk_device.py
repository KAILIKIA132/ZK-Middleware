import logging
from zk import ZK, const
import time

logger = logging.getLogger(__name__)

class ZKDevice:
    def __init__(self, ip, port=4370, timeout=10):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.zk = ZK(self.ip, port=self.port, timeout=self.timeout, password=0)
        self.conn = None

    def connect(self):
        try:
            self.conn = self.zk.connect()
            self.conn.disable_device()
            logger.info("Connected to ZK device %s:%s", self.ip, self.port)
            return True
        except Exception as e:
            logger.exception("Failed to connect to ZK device: %s", e)
            return False

    def disconnect(self):
        try:
            if self.conn:
                self.conn.enable_device()
                self.conn.disconnect()
                self.conn = None
        except Exception:
            pass

    def get_users(self):
        """
        Returns list of user objects (uid, name, user_id)
        """
        if not self.conn:
            if not self.connect():
                return []
        try:
            return self.conn.get_users()
        except Exception as e:
            logger.exception("get_users failed: %s", e)
            return []

    def pull_attendance(self):
        """
        Pull attendance logs from the device. Many devices have get_attendance() / get_logs().
        """
        if not self.conn:
            if not self.connect():
                return []
        try:
            logs = self.conn.get_attendance()
            # logs are typically tuples or objects: (uid, timestamp, status, punch)
            return logs
        except Exception as e:
            logger.exception("pull_attendance failed: %s", e)
            return []

    def live_capture(self, timeout=10):
        """
        For devices supporting live capture, try live_capture (pyzk exposes it)
        Note: behavior depends on device model and pyzk compatibility.
        """
        if not self.conn:
            if not self.connect():
                return None
        try:
            return self.conn.live_capture(timeout)
        except Exception as e:
            logger.exception("live_capture failed: %s", e)
            return None

    def send_display_message(self, message, timeout=5):
        """
        Not all devices support display message via pyzk. This is illustrative.
        If pyzk lacks command, use vendor SDK.
        """
        try:
            # Some devices support 'send_command' or display functions via the SDK only.
            if hasattr(self.conn, 'display_text'):
                self.conn.display_text(message)
                return True
        except Exception as e:
            logger.exception("send_display_message failed: %s", e)
        return False