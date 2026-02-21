import socket		#para crear el socket
import threading	#para el contador
import time		#para el delay

contador_clientes = 0 # recurso compartido
lock = threading.Lock()

def handle_client(conn, addr):
        global contador_clientes

        name = conn.recv(1024).decode()

        # Seccion critica protegida - Incremento del contador
        with lock:
                contador_clientes += 1
                numero = contador_clientes

        print(f"Cliente {numero} en atencion desde {addr}")

        # Simular tiempo de atencion del banco
        time.sleep(10)

        response = f"Hola {name}, eres el cliente numero {numero}"
        conn.sendall(response.encode())

        conn.close()
        print(f"Cliente {numero} finalizado y conexion cerrada con {addr}")


#Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5000))
server.listen()

print("Servidor concurrente con lock y contador escuchando...")

while True:
        conn, addr = server.accept()
        thread = threading.Thread(
                target=handle_client,
                args=(conn, addr)
        )
        thread.start()
