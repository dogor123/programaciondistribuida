import threading
import time

cupos_disponibles = 10

def reservar_sin_lock(usuario_id):
    global cupos_disponibles
    if cupos_disponibles > 0:
        # Simulamos un pequeño retraso para forzar el error de concurrencia
        time.sleep(0.01) 
        cupos_disponibles -= 1
        print(f"Usuario {usuario_id}: Reserva exitosa.")
    else:
        print(f"Usuario {usuario_id}: No hay cupos.")

hilos = []
for i in range(50):
    t = threading.Thread(target=reservar_sin_lock, args=(i,))
    hilos.append(t)
    t.start()

for t in hilos: t.join()

print(f"\nResultado final sin Lock: {cupos_disponibles} cupos restantes.")
