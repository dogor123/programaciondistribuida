import threading

cupos_disponibles = 10
candado = threading.Lock()

def reservar_con_lock(usuario_id):
    global cupos_disponibles
    with candado: # Sección crítica protegida
        if cupos_disponibles > 0:
            cupos_disponibles -= 1
            print(f"Usuario {usuario_id}: Reserva exitosa.")
        else:
            print(f"Usuario {usuario_id}: Agotado.")

hilos = []
for i in range(50):
    t = threading.Thread(target=reservar_con_lock, args=(i,))
    hilos.append(t)
    t.start()

for t in hilos: t.join()

print(f"\nResultado final con Lock: {cupos_disponibles} cupos restantes.")
