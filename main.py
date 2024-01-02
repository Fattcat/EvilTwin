# main.py

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    user_input = request.json['password']

    with open("output.txt", "r") as file:
        saved_password = file.read().strip()

    if user_input == saved_password:
        message = "Correct password :D"
    else:
        message = "Incorrect password! Please try again."
        # Uncomment the line below to run aircrack-ng with EvilTwin capabilities
        # os.system("aircrack-ng MyWiFiHandShake.cap -w output.txt --evil-twin")

    return jsonify({'message': message})

if __name__ == "__main__":
    app.run(debug=True)
