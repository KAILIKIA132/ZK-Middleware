import logging
# Try different import methods for pyzk
try:
    from zk import ZK, const
except ImportError:
    try:
        from pyzk.zk import ZK, const
    except ImportError:
        try:
            from pyzk import ZK, const
        except ImportError:
            # Fallback to mock implementation for development
            ZK = None
            const = None
            logging.warning("pyzk library not available, using mock implementation")

import time

logger = logging.getLogger(__name__)

class ZKDevice:
    def __init__(self, ip, port=4370, timeout=10):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        # Only create ZK instance if the library is available
        if ZK is not None:
            self.zk = ZK(self.ip, port=self.port, timeout=self.timeout, password=0)
        else:
            self.zk = None
        self.conn = None
        self._connected = False

    def connect(self):
        # Return False if pyzk is not available
        if self.zk is None:
            logger.warning("pyzk library not available, cannot connect to device")
            return False
            
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
            if self.conn and hasattr(self.conn, 'enable_device'):
                self.conn.enable_device()
            if self.conn and hasattr(self.conn, 'disconnect'):
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
        # Return empty list if pyzk is not available
        if self.zk is None:
            logger.warning("pyzk library not available, returning empty user list")
            return []
            
        if not self._connected:
            if not self.connect():
                return []
        try:
            if self.conn and hasattr(self.conn, 'get_users'):
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
        # Return empty list if pyzk is not available
        if self.zk is None:
            logger.warning("pyzk library not available, returning empty attendance list")
            return []
            
        if not self._connected:
            if not self.connect():
                return []
        try:
            if self.conn and hasattr(self.conn, 'get_attendance'):
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
        # Return None if pyzk is not available
        if self.zk is None:
            logger.warning("pyzk library not available, live capture not supported")
            return None
            
        if not self._connected:
            if not self.connect():
                return None
        try:
            if self.conn and hasattr(self.conn, 'live_capture'):
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
        # Return False if pyzk is not available
        if self.zk is None:
            logger.warning("pyzk library not available, cannot send display message")
            return False
            
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