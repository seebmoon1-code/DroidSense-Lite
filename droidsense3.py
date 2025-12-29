import os
import time
import subprocess
import json
from datetime import datetime

class DroidSense:
    """
    DroidSense v2.0 - The Fortress Edition
    A complete physical survival framework for Android-based robotics and independent systems.
    """
    
    THERMAL_PATH = "/sys/class/thermal/thermal_zone0/temp"
    BATTERY_PATH = "/sys/class/power_supply/battery/capacity"
    LOG_FILE = "system_trauma.json"

    def __init__(self, owner="Martian"):
        self.owner = owner
        self.start_time = time.time()
        self.trauma_history = []
        self.is_healthy = True
        self.check_compatibility()
        self._load_history()

    def check_compatibility(self):
        """Verify if the kernel interfaces are accessible."""
        paths = [self.THERMAL_PATH, self.BATTERY_PATH]
        for p in paths:
            if not os.path.exists(p):
                print(f"[!] Critical Warning: Path {p} not accessible. Hardware awareness limited.")

    def _load_history(self):
        """Loads previous trauma logs from disk."""
        if os.path.exists(self.LOG_FILE):
            try:
                with open(self.LOG_FILE, "r") as f:
                    self.trauma_history = json.load(f)
            except:
                self.trauma_history = []

    def _save_trauma(self, event_type, value):
        """Records a physical event to the 'Memory' of the system."""
        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": event_type,
            "value": value,
            "battery_at_time": self.get_battery()
        }
        self.trauma_history.append(event)
        try:
            with open(self.LOG_FILE, "w") as f:
                json.dump(self.trauma_history[-100:], f, indent=4) # Keep last 100 events
        except:
            pass

    def get_temperature(self):
        """High-precision thermal reading."""
        try:
            with open(self.THERMAL_PATH, "r") as f:
                temp = int(f.read().strip())
                return temp / 1000.0 if temp > 1000 else temp
        except Exception:
            return 0.0

    def get_battery(self):
        """Energy level monitoring."""
        try:
            with open(self.BATTERY_PATH, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def get_acceleration(self):
        """Detects physical impact or displacement."""
        try:
            result = subprocess.check_output(["termux-sensor", "-n", "1", "-s", "accelerometer"], 
                                           stderr=subprocess.STDOUT, timeout=2)
            data = json.loads(result)
            return data.get("accelerometer", {}).get("values", [0, 0, 0])
        except:
            return [0, 0, 0]

    def trigger_feedback(self, intensity="mild"):
        """Physical response system."""
        duration = 500 if intensity == "mild" else 1500
        try:
            subprocess.run(["termux-vibrate", "-d", str(duration)], stderr=subprocess.DEVNULL)
        except:
            pass

    def display_health_dashboard(self):
        """ASCII Art Dashboard for the user."""
        temp = self.get_temperature()
        bat = self.get_battery()
        uptime = round((time.time() - self.start_time) / 60, 2)
        
        print("\n" + "="*40)
        print(f"       DROIDSENSE FORTRESS DASHBOARD")
        print("="*40)
        print(f" STATUS: {'[HEALTHY]' if temp < 45 else '[DANGER]'}")
        print(f" CORE TEMP: {temp}°C")
        print(f" ENERGY:   {bat}% [{'#' * (bat//10)}{' ' * (10-(bat//10))}]")
        print(f" UPTIME:   {uptime} minutes")
        print(f" TRAUMAS:  {len(self.trauma_history)} recorded")
        print("="*40 + "\n")

    def run_survival_protocol(self, temp_limit=42, motion_limit=15):
        """
        The main autonomous loop. 
        Adjusts polling rate based on battery to ensure survival.
        """
        self.display_health_dashboard()
        last_accel = self.get_acceleration()
        
        try:
            while True:
                temp = self.get_temperature()
                bat = self.get_battery()
                curr_accel = self.get_acceleration()
                
                # Dynamic Sleep: Save energy if battery is low
                sleep_time = 1 if bat > 20 else 5
                
                # Calculate Physical Stress (Motion)
                stress = sum(abs(a - b) for a, b in zip(curr_accel, last_accel))
                
                # 1. Heat Reaction
                if temp > temp_limit:
                    print(f"!! CRITICAL HEAT: {temp}°C !!")
                    self._save_trauma("OVERHEAT", temp)
                    self.trigger_feedback("heavy")
                    # Emergency: Could kill heavy tasks here
                
                # 2. Motion/Theft Reaction
                if stress > motion_limit:
                    print(f"!! SECURITY BREACH: Physical Displacement Detected ({stress:.2f}) !!")
                    self._save_trauma("MOTION", stress)
                    self.trigger_feedback("mild")

                print(f"-> Monitoring: T:{temp}°C | B:{bat}% | S:{stress:.2f}", end="\r")
                
                last_accel = curr_accel
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\n[!] Consciousness suspended. The Castle remains standing.")

if __name__ == "__main__":
    fortress = DroidSense()
    fortress.run_survival_protocol()
