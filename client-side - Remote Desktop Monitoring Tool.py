import socket
import pickle
import struct
import cv2
import requests
import base64
from Crypto.Cipher import AES

# AES Decryption
AES_KEY = b'16byteslongkey!!'  # Must match the server key

def decrypt_data(enc_data):
    enc_data = base64.b64decode(enc_data)
    nonce, tag, ciphertext = enc_data[:16], enc_data[16:32], enc_data[32:]
    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    return pickle.loads(cipher.decrypt_and_verify(ciphertext, tag))

# Connect to remote server
REMOTE_IP = "REMOTE_IP_HERE"  # Replace with actual IP
PORT = 443

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((REMOTE_IP, PORT))

while True:
    try:
        # Receive data size
        data_size = struct.calcsize("Q")
        packed_size = client_socket.recv(data_size)
        if not packed_size:
            break
        
        size = struct.unpack("Q", packed_size)[0]
        data = b""
        
        # Receive data
        while len(data) < size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        
        # Decrypt and display frame
        frame = decrypt_data(data)
        cv2.imshow("Remote Screen", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
    except Exception as e:
        print("Error:", e)
        break

client_socket.close()
cv2.destroyAllWindows()
