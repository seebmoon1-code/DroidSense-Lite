
#!/bin/bash

# DroidSense Installation Script
# Designed for Android Independence

echo "------------------------------------------"
echo "   DroidSense: Initializing Awareness    "
echo "------------------------------------------"

# 1. Update system packages
echo "[+] Updating package list..."
pkg update -y && pkg upgrade -y

# 2. Install Python if not present
if ! command -v python &> /dev/null
then
    echo "[+] Python not found. Installing..."
    pkg install python -y
else
    echo "[!] Python is already installed."
fi

# 3. Check for Linux Kernel access (Thermal/Battery)
echo "[+] Checking hardware accessibility..."
if [ -d "/sys/class/thermal" ]; then
    echo "[-] Thermal sensors: ACCESSIBLE"
else
    echo "[!] Warning: Thermal path not standard. DroidSense might need root or specific kernel."
fi

if [ -d "/sys/class/power_supply/battery" ]; then
    echo "[-] Battery sensors: ACCESSIBLE"
else
    echo "[!] Warning: Battery path not found."
fi

# 4. Set execution permissions for the main script
if [ -f "droidsense.py" ]; then
    chmod +x droidsense.py
    echo "[+] Permissions set for droidsense.py"
else
    echo "[!] Error: droidsense.py not found in current directory!"
fi

echo "------------------------------------------"
echo "Setup Complete. To start the 'Experience':"
echo "python droidsense.py"
echo "------------------------------------------"
