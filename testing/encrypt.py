import os
import time
from cryptography.fernet import Fernet

# Generate a key based on the current time
key = str(int(time.time())).encode()

# Create a Fernet cipher with the generated key
cipher = Fernet(key)

# Read the file to be encrypted
with open('file_to_encrypt.txt', 'rb') as file:
    plaintext = file.read()

# Encrypt the file using the Fernet cipher
ciphertext = cipher.encrypt(plaintext)

# Send the encrypted file over the network (example using a socket)
import socket
s = socket.socket()
host = '192.168.1.1'  # Replace with the destination IP address
port = 12345  # Replace with a free port number on the destination machine
s.connect((host, port))
s.send(ciphertext)
s.close()

# To decrypt the file on the other computer, use the same key
cipher = Fernet(key)

# Receive the encrypted file over the network (example using a socket)
import socket
s = socket.socket()
host = ''  # Leave blank to accept connections on all available interfaces
port = 12345  # Replace with the same port number used for sending
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
ciphertext = conn.recv(1024)
conn.close()

# Decrypt the file using the Fernet cipher
plaintext = cipher.decrypt(ciphertext)

# Write the decrypted file to disk
with open('decrypted_file.txt', 'wb') as file:
    file.write(plaintext)
