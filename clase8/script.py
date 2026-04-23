import requests
import threading

def hacer_peticion():
    response = requests.post("http://localhost:8000/crear_cita/2pm")
    print(response.text)

threads = []

for _ in range(5):
    t = threading.Thread(target=hacer_peticion)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
