import threading
import time

# Paso 1: crear variable global y el Lock
asientos = 10
lock = threading.Lock()

# Paso 2 y 4: crear función de reserva protegiendo la sección crítica
def reservar(id_usuario):
    global asientos

    # Usamos "with lock" para asegurar que solo un hilo entre a la vez
    with lock:
        if asientos > 0:
            # Simulamos un pequeño retraso para ver la concurrencia en acción
            time.sleep(0.1)
            asientos -= 1
            print(f"Usuario {id_usuario}: Reserva exitosa. Asientos restantes: {asientos}")
        else:
            print(f"Usuario {id_usuario}: Agotado. No hay asientos disponibles.")

# Paso 3: crear múltiples hilos (simulación de 50 usuarios)
hilos = []
for i in range(50):
    hilo = threading.Thread(target=reservar, args=(i,))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

print(f"\nSimulación terminada. Asientos finales: {asientos}")
