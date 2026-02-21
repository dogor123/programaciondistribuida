import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

name = input("Ingrese su nombre: ")
client.sendall(name.encode())

response = client.recv(1024).decode()
print(response)

client.close()
