import os
import requests
from bs4 import BeautifulSoup
import threading
import time
import json

class RoboScout:
    """
    RoboScout v1.0 - The Crawler and Data Harvester.
    Can crawl the web for news or scout the local filesystem for target files.
    """
    def __init__(self, agent_name="Scout-01"):
        self.agent_name = agent_name
        self.results = []
        self.is_hunting = False

    def log(self, message):
        print(f"[+] [{self.agent_name}] {message}")

    # --- بخش اول: خزنده وب (Web Crawler) ---
    def web_scout(self, url, keyword):
        """Searches a website for specific keywords and extracts links."""
        try:
            self.log(f"Scouting web: {url} for '{keyword}'")
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_items = []
            for link in soup.find_all('a'):
                text = link.text.strip()
                href = link.get('href')
                if keyword.lower() in text.lower():
                    found_items.append({"text": text, "url": href})
            
            self.results.extend(found_items)
            return found_items
        except Exception as e:
            self.log(f"Web Scout failed: {e}")
            return []

    # --- بخش دوم: خزنده سیستم (File Scout) ---
    def file_scout(self, start_path, extension):
        """Scans the Android filesystem for specific file types (e.g., .pdf, .py)."""
        self.log(f"Scouting files in {start_path} for {extension} files...")
        matches = []
        for root, dirs, files in os.walk(start_path):
            for file in files:
                if file.endswith(extension):
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        
        self.results.extend(matches)
        return matches

    # --- بخش سوم: عملیات مخفیانه (Autonomous Mode) ---
    def start_autonomous_hunt(self, targets, interval=60):
        """Repeatedly scouts targets in the background."""
        self.is_hunting = True
        def hunt():
            while self.is_hunting:
                for target_url, key in targets.items():
                    res = self.web_scout(target_url, key)
                    if res:
                        self.log(f"New Intel Found: {len(res)} items")
                time.sleep(interval)
        
        threading.Thread(target=hunt, daemon=True).start()

    def export_intelligence(self, filename="intelligence_report.json"):
        """Saves all found data into a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        self.log(f"Intelligence exported to {filename}")

# --- مثال برای دانشجوها ---
if __name__ == "__main__":
    scout = RoboScout(agent_name="Neptune-Scout")
    
    # جستجو در وب برای اخبار رباتیک
    # scout.web_scout("https://news.ycombinator.com", "robot")
    
    # جستجو در گوشی برای فایل‌های پایتون
    # scout.file_scout("/sdcard/", ".py")
    
    print("Scout is ready for mission.")
