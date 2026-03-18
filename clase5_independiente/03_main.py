import threading
import time

cupos_disponibles = 10
semaforo = threading.Semaphore(3) # Permite 3 reservas simultáneas

def reservar_con_semaforo(usuario_id):
    global cupos_disponibles
    
    with semaforo: # Entran hasta 3 usuarios a la vez
        print(f"--- Usuario {usuario_id} está procesando su reserva ---")
        time.sleep(0.5) # Simula procesamiento
        if cupos_disponibles > 0:
            cupos_disponibles -= 1
            print(f"Usuario {usuario_id}: ¡Reserva completada!")
        else:
            print(f"Usuario {usuario_id}: Ya no hay lugares.")

hilos = []
for i in range(50):
    t = threading.Thread(target=reservar_con_semaforo, args=(i,))
    hilos.append(t)
    t.start()

for t in hilos: t.join()
