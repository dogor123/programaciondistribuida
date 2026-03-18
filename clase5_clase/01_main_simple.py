import threading

saldo = 100

def retirar():
    global saldo
    
    for i in range(1000):
        saldo = saldo - 1

hilo1 = threading.Thread(target=retirar)
hilo2 = threading.Thread(target=retirar)

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print(saldo)
