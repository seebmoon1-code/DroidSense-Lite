import os
import time

class DroidSense:
    """
    A library to give Python scripts 'physical awareness' on Android
    by communicating directly with the Linux kernel files.
    """
    
    THERMAL_PATH = "/sys/class/thermal/thermal_zone0/temp"
    BATTERY_PATH = "/sys/class/power_supply/battery/capacity"

    def __init__(self):
        self.check_compatibility()

    def check_compatibility(self):
        if not os.path.exists(self.THERMAL_PATH):
            print("[!] Warning: Thermal path not found. Is this an Android device?")

    def get_temperature(self):
        """Returns the CPU temperature in Celsius."""
        try:
            with open(self.THERMAL_PATH, "r") as f:
                temp = int(f.read().strip())
                # Some kernels return milli-Celsius
                return temp / 1000.0 if temp > 1000 else temp
        except Exception as e:
            return f"Error reading temp: {e}"

    def get_battery(self):
        """Returns the battery percentage."""
        try:
            with open(self.BATTERY_PATH, "r") as f:
                return int(f.read().strip())
        except Exception as e:
            return f"Error reading battery: {e}"

    def monitor_survival(self, temp_threshold=45):
        """
        Logic based on your 'Neptune' analogy: 
        The system reacts if it 'feels' it's burning.
        """
        print("Monitoring physical health...")
        try:
            while True:
                temp = self.get_temperature()
                bat = self.get_battery()
                
                status = f"Temp: {temp}°C | Battery: {bat}%"
                print(status, end="\r")

                if isinstance(temp, float) and temp > temp_threshold:
                    print(f"\n[ALERT] System is burning! ({temp}°C)")
                    print("Taking autonomous action to save the 'Castle'...")
                    # Add logic to kill heavy processes or notify user
                    break
                
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    device = DroidSense()
    print(f"Initial Health Check - Battery: {device.get_battery()}%")
    device.monitor_survival(temp_threshold=40)
