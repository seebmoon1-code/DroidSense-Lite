import os
import time
import subprocess
import json

class DroidSense:
    """
    DroidSense v1.2 - The 'Guardian' Version
    Gives your Android device a physical instinct for survival.
    """
    
    THERMAL_PATH = "/sys/class/thermal/thermal_zone0/temp"
    BATTERY_PATH = "/sys/class/power_supply/battery/capacity"

    def __init__(self):
        self.check_compatibility()

    def check_compatibility(self):
        if not os.path.exists(self.THERMAL_PATH):
            print("[!] Warning: Thermal path not found. Some features may be limited.")

    def get_temperature(self):
        """Returns the CPU temperature in Celsius."""
        try:
            with open(self.THERMAL_PATH, "r") as f:
                temp = int(f.read().strip())
                return temp / 1000.0 if temp > 1000 else temp
        except Exception:
            return 0.0

    def get_battery(self):
        """Returns the battery percentage."""
        try:
            with open(self.BATTERY_PATH, "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def trigger_physical_pain(self):
        """Uses Termux-API to vibrate. The hardware's response to trauma."""
        try:
            subprocess.run(["termux-vibrate", "-d", "1000"], stderr=subprocess.DEVNULL) 
            print("\n[!] Physical feedback triggered: Vibration")
        except FileNotFoundError:
            pass # Termux-API not installed

    def get_acceleration(self):
        """Reads accelerometer data to detect if the 'Castle' is moved."""
        try:
            # Requires termux-api package
            result = subprocess.check_output(["termux-sensor", "-n", "1", "-s", "accelerometer"], stderr=subprocess.STDOUT)
            data = json.loads(result)
            # Accessing the first sensor reading
            accel = data.get("accelerometer", {}).get("values", [0, 0, 0])
            return accel 
        except Exception:
            return [0, 0, 0]

    def monitor_survival(self, temp_threshold=42, motion_threshold=15):
        """The main consciousness loop."""
        print("--- DroidSense Guardian Mode Active ---")
        print(f"Thresholds: Temp > {temp_threshold}C | Motion > {motion_threshold}")
        
        last_accel = self.get_acceleration()
        
        try:
            while True:
                temp = self.get_temperature()
                bat = self.get_battery()
                current_accel = self.get_acceleration()
                
                # Calculate movement intensity (Difference between last and current)
                movement = sum(abs(a - b) for a, b in zip(current_accel, last_accel))
                
                status = f"Temp: {temp}°C | Bat: {bat}% | Motion: {movement:.2f}"
                print(status, end="\r")

                # 1. Thermal Awareness (The 'Burning' Sensation)
                if temp > temp_threshold:
                    print(f"\n[ALERT] System is burning! ({temp}°C)")
                    self.trigger_physical_pain()
                    time.sleep(1) # Prevent constant vibration

                # 2. Motion Awareness (The 'Security' Instinct)
                if movement > motion_threshold:
                    print(f"\n[SECURITY] Motion detected! The Castle is under movement.")
                    self.trigger_physical_pain()
                
                last_accel = current_accel
                time.sleep(1) # Refresh rate

        except KeyboardInterrupt:
            print("\nMonitoring stopped. The Castle is now silent.")

if __name__ == "__main__":
    device = DroidSense()
    # Start the monitoring with default thresholds
    device.monitor_survival(temp_threshold=43, motion_threshold=12)
