import threading
import requests
import random
import time

# Configuración: Reemplaza con tu IP si tus compañeros se van a conectar
URL_BASE = "http://localhost:8000" 

def simulacion_usuario(id_usuario):
    nombre = f"Usuario_{id_usuario}"
    
    # 1. Registrar usuario
    try:
        requests.post(f"{URL_BASE}/usuarios?nombre={nombre}")
        
        # 2. Enviar un mensaje a la sala (Chat Centralizado)
        msg_sala = f"Hola a todos, soy {nombre} participando en el sistema distribuido"
        requests.post(f"{URL_BASE}/mensajes?remitente_id={id_usuario}&contenido={msg_sala}")
        
        # 3. Simular un delay de red (Clase 2)
        time.sleep(random.uniform(0.1, 0.5))
        
        # 4. Enviar un mensaje privado a otro usuario aleatorio (Nodo a Nodo)
        destinatario = random.randint(1, 50)
        if destinatario != id_usuario:
            msg_privado = f"Oye {destinatario}, este es un mensaje secreto de {id_usuario}"
            requests.post(
                f"{URL_BASE}/mensaje_privado?remitente_id={id_usuario}&destinatario_id={destinatario}&contenido={msg_privado}"
            )
            print(f"✅ {nombre} envió mensajes con éxito.")

    except Exception as e:
        print(f"❌ Error en {nombre}: {e}")

# Crear 50 hilos (Clase 5)
hilos = []
for i in range(1, 51):
    t = threading.Thread(target=simulacion_usuario, args=(i,))
    hilos.append(t)
    t.start()

for t in hilos:
    t.join()

print("\n--- Simulación de 50 usuarios completada ---")
