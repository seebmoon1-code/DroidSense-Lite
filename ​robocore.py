import time
import threading
from datetime import datetime

class RoboCore:
    """
    RoboCore v1.0 - The Central Nervous System for Autonomous Robots.
    Features: Multi-tasking, Shared Memory, and Emergency Protocols.
    """
    def __init__(self):
        self.tasks = {}
        self.memory = {} # Shared memory for sensors and actuators
        self.running = False
        self.lock = threading.Lock() # Prevents data corruption

    def write_memory(self, key, value):
        """Safely write data to shared robot memory."""
        with self.lock:
            self.memory[key] = value

    def read_memory(self, key, default=None):
        """Safely read data from shared robot memory."""
        with self.lock:
            return self.memory.get(key, default)

    def add_task(self, name, function, interval):
        """Adds a recurring task. Function should be the task logic."""
        self.tasks[name] = {
            'func': function, 
            'int': interval, 
            'last': 0,
            'count': 0
        }
        print(f"[+] Task '{name}' registered (Interval: {interval}s)")

    def log(self, message):
        """Standardized robot logging with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [RoboCore] {message}")

    def _run_loop(self):
        self.log("Nervous System: ONLINE")
        while self.running:
            for name, task in self.tasks.items():
                if time.time() - task['last'] >= task['int']:
                    # Use daemon threads so they close when main program exits
                    t = threading.Thread(target=self._execute_task, args=(name, task['func']))
                    t.daemon = True
                    t.start()
                    task['last'] = time.time()
                    task['count'] += 1
            time.sleep(0.005) # High precision sleep

    def _execute_task(self, name, func):
        try:
            func()
        except Exception as e:
            self.log(f"Critical Error in task '{name}': {e}")

    def start(self):
        """Launches the robot's consciousness."""
        if not self.running:
            self.running = True
            self.main_thread = threading.Thread(target=self._run_loop)
            self.main_thread.daemon = True
            self.main_thread.start()

    def stop(self):
        """Emergency stop for all systems."""
        self.running = False
        self.log("Emergency Stop: ALL SYSTEMS OFFLINE")

# --- Full Implementation Example ---
if __name__ == "__main__":
    core = RoboCore()

    # 1. Define a Sensor Task (Writing to memory)
    def lora_sensor():
        dist = 25 # Imagine reading from hardware
        core.write_memory("distance", dist)
    
    # 2. Define an Actuator Task (Reading from memory)
    def motor_controller():
        d = core.read_memory("distance", 100)
        if d < 30:
            core.log("Object detected! Braking...")

    # Registering tasks
    core.add_task("Eye", lora_sensor, 0.5)
    core.add_task("Legs", motor_controller, 0.1)

    # Start the robot
    core.start()

    # Keep main program alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        core.stop()
