import socket
import sys
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

# nombre automatico usando argumento
name = sys.argv[1]

client.sendall(name.encode())

response = client.recv(1024).decode()

print(f"{name}: {response}")

client.close()
