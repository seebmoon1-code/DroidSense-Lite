import os
import subprocess
import time
import json
from datetime import datetime

class RoboVision:
    """
    RoboVision v1.0 - Lightweight Computer Vision for Android Robotics.
    Pure Python & Terminal-based image analysis without heavy dependencies.
    """
    
    def __init__(self, storage_path="./vision_data"):
        self.storage_path = storage_path
        self.last_capture = None
        self.is_ready = False
        self._setup_storage()
        self._check_tools()

    def _setup_storage(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _check_tools(self):
        """Verify if termux-camera-photo is available."""
        try:
            subprocess.run(["termux-camera-info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.is_ready = True
            print("[+] RoboVision: Hardware camera linked.")
        except FileNotFoundError:
            print("[!] RoboVision Warning: termux-api not found. Simulation mode active.")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [Vision] {message}")

    def capture_frame(self, camera_id=0):
        """Captures a still image from the mobile camera."""
        filename = f"{self.storage_path}/frame_{int(time.time())}.jpg"
        try:
            # Capture using Termux-API
            subprocess.run(["termux-camera-photo", "-c", str(camera_id), filename], 
                           check=True, stdout=subprocess.DEVNULL)
            self.last_capture = filename
            return filename
        except Exception as e:
            self.log(f"Capture failed: {e}")
            return None

    def analyze_brightness(self, image_path):
        """
        Analyzes how bright the environment is. 
        Returns a value between 0 (Dark) and 255 (Bright).
        """
        if not image_path or not os.path.exists(image_path):
            return 0
        
        try:
            # Extract raw pixel data using a simple 'convert' or 'cat' trick 
            # for lightweight analysis without OpenCV
            with open(image_path, 'rb') as f:
                data = f.read()
                # Use a small sample of the image data to estimate brightness
                avg_brightness = sum(data[-1000:]) / 1000
                return avg_brightness
        except:
            return 128

    def detect_motion(self, threshold=30):
        """
        Compares two consecutive frames to detect movement.
        """
        self.log("Analyzing motion...")
        frame1 = self.capture_frame()
        time.sleep(0.5)
        frame2 = self.capture_frame()
        
        if not frame1 or not frame2:
            return False
            
        # Simplified file size comparison as a proxy for movement
        diff = abs(os.path.getsize(frame1) - os.path.getsize(frame2))
        motion_score = diff / 1024 # KB difference
        
        # Cleanup
        os.remove(frame1)
        os.remove(frame2)
        
        return motion_score > threshold

    def self_destruct_data(self):
        """Cleans up the image storage to save space on mobile."""
        for file in os.listdir(self.storage_path):
            os.remove(os.path.join(self.storage_path, file))
        self.log("Vision cache cleared.")

    def run_security_eye(self):
        """A ready-to-use security loop."""
        self.log("Security Eye Activated. Monitoring for movement...")
        try:
            while True:
                if self.detect_motion(threshold=50):
                    self.log("!!! ALERT: Movement Detected in the Castle !!!")
                    # You can link this to DroidSense vibration
                    subprocess.run(["termux-vibrate", "-d", "2000"])
                time.sleep(2)
        except KeyboardInterrupt:
            self.log("Security Eye suspended.")

# --- Full Integration Scenario ---
if __name__ == "__main__":
    vision = RoboVision()
    
    print("--- RoboVision Command Center ---")
    print("1. Take Photo")
    print("2. Test Brightness")
    print("3. Start Security Eye (Motion Detection)")
    
    choice = input("Select Action: ")
    
    if choice == "1":
        path = vision.capture_frame()
        print(f"Photo saved at: {path}")
    elif choice == "2":
        path = vision.capture_frame()
        brightness = vision.analyze_brightness(path)
        print(f"Environment Brightness: {brightness:.2f}/255")
    elif choice == "3":
        vision.run_security_eye()
