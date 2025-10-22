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
        self._connected = False

    def connect(self):
        try:
            self.conn = self.zk.connect()
            if self.conn:
                self.conn.disable_device()
                self._connected = True
                logger.info("Connected to ZK device %s:%s", self.ip, self.port)
                return True
            else:
                self._connected = False
                logger.error("Failed to establish connection to ZK device")
                return False
        except Exception as e:
            self._connected = False
            logger.exception("Failed to connect to ZK device: %s", e)
            return False

    def disconnect(self):
        try:
            if self.conn:
                self.conn.enable_device()
                self.conn.disconnect()
        except Exception as e:
            logger.exception("Error disconnecting from ZK device: %s", e)
        finally:
            self.conn = None
            self._connected = False

    def get_users(self):
        """
        Returns list of user objects (uid, name, user_id)
        """
        if not self._connected:
            if not self.connect():
                return []
        try:
            if self.conn:
                return self.conn.get_users()
            else:
                return []
        except Exception as e:
            logger.exception("get_users failed: %s", e)
            # Try to reconnect
            self._connected = False
            return []

    def pull_attendance(self):
        """
        Pull attendance logs from the device. Many devices have get_attendance() / get_logs().
        """
        if not self._connected:
            if not self.connect():
                return []
        try:
            if self.conn:
                logs = self.conn.get_attendance()
                # logs are typically tuples or objects: (uid, timestamp, status, punch)
                return logs
            else:
                return []
        except Exception as e:
            logger.exception("pull_attendance failed: %s", e)
            # Try to reconnect
            self._connected = False
            return []

    def live_capture(self, timeout=10):
        """
        For devices supporting live capture, try live_capture (pyzk exposes it)
        Note: behavior depends on device model and pyzk compatibility.
        """
        if not self._connected:
            if not self.connect():
                return None
        try:
            if self.conn:
                return self.conn.live_capture(timeout)
            else:
                return None
        except Exception as e:
            logger.exception("live_capture failed: %s", e)
            # Try to reconnect
            self._connected = False
            return None

    def send_display_message(self, message, timeout=5):
        """
        Not all devices support display message via pyzk. This is illustrative.
        If pyzk lacks command, use vendor SDK.
        """
        if not self._connected:
            return False
            
        try:
            # Some devices support 'send_command' or display functions via the SDK only.
            if self.conn and hasattr(self.conn, 'display_text'):
                self.conn.display_text(message)
                return True
            else:
                return False
        except Exception as e:
            logger.exception("send_display_message failed: %s", e)
            return False