import socket
import threading
import time

class RoboAir:
    """
    RoboAir v1.0 - Zero-Config Wireless Bridge.
    Enables devices to talk to each other without a router or internet.
    Uses UDP Broadcasting for peer-to-peer communication.
    """
    def __init__(self, port=5005):
        self.port = port
        self.running = False
        self.received_messages = []
        self.lock = threading.Lock()

    def start(self):
        """Starts listening for messages from other robots."""
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", self.port))
        
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        print(f"[*] RoboAir: Signal Listening on port {self.port}")

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode('utf-8')
                with self.lock:
                    self.received_messages.append({"sender": addr[0], "msg": message})
                    print(f"\n[Incoming Signal] From {addr[0]}: {message}")
            except Exception:
                pass

    def broadcast(self, message):
        """Sends a message to EVERYONE on the local network."""
        try:
            broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            broadcast_sock.sendto(message.encode('utf-8'), ('255.255.255.255', self.port))
            broadcast_sock.close()
            return True
        except Exception as e:
            print(f"[!] Broadcast Error: {e}")
            return False

    def get_inbox(self):
        """Returns and clears the inbox of messages."""
        with self.lock:
            messages = list(self.received_messages)
            self.received_messages = []
            return messages

    def stop(self):
        self.running = False
        print("[*] RoboAir: Signal Offline.")

# --- How to use for Robot Teamwork ---
if __name__ == "__main__":
    air = RoboAir()
    air.start()
    
    # Send a pulse every 5 seconds
    try:
        while True:
            air.broadcast("Robot-Alpha: Standing by.")
            time.sleep(5)
    except KeyboardInterrupt:
        air.stop()
