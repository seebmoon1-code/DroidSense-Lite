import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime

class RoboLink:
    """
    RoboLink v1.5 - Ultra Smart Serial Bridge.
    Features: Auto-Discovery, Auto-Reconnect, and Non-blocking I/O.
    Designed for independent robotics development.
    """
    def __init__(self, port=None, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None
        self.running = False
        self.last_message = ""
        self.lock = threading.Lock()

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [RoboLink] {message}")

    def discover_ports(self):
        """Automatically find available serial ports."""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            self.log(f"Found Device: {p.device}")
        return [p.device for p in ports]

    def connect(self):
        """Connect with auto-retry logic."""
        if not self.port:
            available = self.discover_ports()
            if not available:
                self.log("No devices found. Check your USB connection.")
                return False
            self.port = available[0] # Take the first one

        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.running = True
            # Listening thread
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
            self.log(f"Connected to {self.port} at {self.baudrate} baud.")
            return True
        except Exception as e:
            self.log(f"Connection failed: {e}")
            return False

    def _listen(self):
        """Continuous background listener with auto-reconnect."""
        while self.running:
            try:
                if self.connection and self.connection.is_open:
                    if self.connection.in_waiting > 0:
                        with self.lock:
                            line = self.connection.readline().decode('utf-8', errors='ignore').rstrip()
                            if line:
                                self.last_message = line
                else:
                    self.log("Connection lost. Retrying in 3s...")
                    time.sleep(3)
                    self.connect()
            except Exception:
                time.sleep(1)
            time.sleep(0.01)

    def send(self, command):
        """Send data safely."""
        if self.connection and self.connection.is_open:
            try:
                with self.lock:
                    full_command = (str(command) + '\n').encode('utf-8')
                    self.connection.write(full_command)
                return True
            except Exception as e:
                self.log(f"Send error: {e}")
        return False

    def get_latest(self):
        """Fetch latest sensor data from hardware."""
        with self.lock:
            return self.last_message

    def disconnect(self):
        self.running = False
        if self.connection:
            self.connection.close()
            self.log("System offline.")

# --- Professional Student Example ---
if __name__ == "__main__":
    # 1. Initialize link (it will try to auto-find port)
    link = RoboLink(baudrate=9600) 
    
    if link.connect():
        try:
            while True:
                # 2. Send command to Arduino
                link.send("GET_SENSORS")
                
                # 3. Read response
                data = link.get_latest()
                if data:
                    print(f"Data from Robot: {data}")
                
                time.sleep(1)
        except KeyboardInterrupt:
            link.disconnect()
