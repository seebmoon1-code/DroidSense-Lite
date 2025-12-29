import socket
import threading
import time
import json
from datetime import datetime

class RoboAir:
    """
    RoboAir v2.0 - Advanced Peer-to-Peer Robotic Networking.
    Features: Device Discovery, Heartbeat Monitoring, and Targeted Messaging.
    """
    def __init__(self, port=5005, node_name="Unnamed-Robot"):
        self.port = port
        self.node_name = node_name
        self.node_id = f"{node_name}-{socket.gethostname()}"
        self.running = False
        self.peers = {}  # { 'ip': {'name': name, 'last_seen': time} }
        self.inbox = []
        self.subscriptions = set()
        self.lock = threading.Lock()

    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [RoboAir] {message}")

    def start(self):
        """Initializes the wireless node."""
        self.running = True
        try:
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.server_sock.bind(("", self.port))
            
            # Threads for listening and housekeeping
            threading.Thread(target=self._listen, daemon=True).start()
            threading.Thread(target=self._heartbeat_loop, daemon=True).start()
            threading.Thread(target=self._cleanup_peers, daemon=True).start()
            
            self.log(f"Node '{self.node_id}' is ONLINE on port {self.port}")
        except Exception as e:
            self.log(f"Failed to start: {e}")

    def _listen(self):
        """Internal receiver with protocol parsing."""
        while self.running:
            try:
                data, addr = self.server_sock.recvfrom(2048)
                payload = json.loads(data.decode('utf-8'))
                sender_ip = addr[0]

                if payload.get("id") == self.node_id:
                    continue # Ignore own broadcasts

                with self.lock:
                    # Update Peer List
                    self.peers[sender_ip] = {
                        "name": payload.get("name"),
                        "last_seen": time.time()
                    }
                    
                    # Process Message
                    if payload["type"] == "chat":
                        self.inbox.append({
                            "from": payload["name"],
                            "ip": sender_ip,
                            "msg": payload["data"],
                            "time": datetime.now().strftime("%H:%M")
                        })
                        self.log(f"Message from {payload['name']}: {payload['data']}")
            except Exception:
                pass

    def _heartbeat_loop(self):
        """Announce presence to the network periodically."""
        while self.running:
            self.announce()
            time.sleep(5)

    def _cleanup_peers(self):
        """Remove robots that haven't responded for 15 seconds."""
        while self.running:
            now = time.time()
            with self.lock:
                expired = [ip for ip, info in self.peers.items() if now - info['last_seen'] > 15]
                for ip in expired:
                    self.log(f"Robot at {ip} ({self.peers[ip]['name']}) went OFFLINE.")
                    del self.peers[ip]
            time.sleep(5)

    def announce(self):
        """Broadcast presence to all peers."""
        packet = {
            "id": self.node_id,
            "name": self.node_name,
            "type": "heartbeat"
        }
        self._send_raw(packet, '255.255.255.255')

    def send_message(self, message, target_ip='255.255.255.255'):
        """Send a text message to a specific IP or broadcast to all."""
        packet = {
            "id": self.node_id,
            "name": self.node_name,
            "type": "chat",
            "data": message
        }
        return self._send_raw(packet, target_ip)

    def _send_raw(self, packet, target_ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.sendto(json.dumps(packet).encode('utf-8'), (target_ip, self.port))
            return True
        except Exception as e:
            self.log(f"Send error: {e}")
            return False

    def get_peers(self):
        """Returns list of currently active robots in the network."""
        with self.lock:
            return list(self.peers.values())

    def stop(self):
        self.running = False
        self.log("Node shutting down...")

# --- Scenario: Swarm Coordination ---
if __name__ == "__main__":
    name = input("Enter Robot Name: ")
    robot = RoboAir(node_name=name)
    robot.start()

    try:
        while True:
            print(f"\n--- {name} Control Menu ---")
            print("1. List Online Robots")
            print("2. Broadcast Message")
            print("3. Check Inbox")
            print("4. Exit")
            choice = input("Select: ")

            if choice == "1":
                peers = robot.get_peers()
                print(f"Online Peers ({len(peers)}): {peers}")
            elif choice == "2":
                msg = input("Enter message: ")
                robot.send_message(msg)
            elif choice == "3":
                print(f"Inbox: {robot.inbox}")
                robot.inbox = []
            elif choice == "4":
                break
    except KeyboardInterrupt:
        pass
    finally:
        robot.stop()
