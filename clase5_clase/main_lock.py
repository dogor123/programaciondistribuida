import threading

saldo = 100
lock = threading.Lock()

def retirar():

    global saldo
    
    for i in range(1000):
    
        lock.acquire()  # entrar a sección crítica
        
        saldo = saldo - 1
        
        lock.release()  # salir de sección crítica

hilo1 = threading.Thread(target=retirar)
hilo2 = threading.Thread(target=retirar)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print(saldo)
