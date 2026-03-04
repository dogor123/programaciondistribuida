Actividades realizadas:

1. Ejercicio del banco multicliente concurrente con contador.
2. Ejercicio del banco multicliente concurrente con contador y Lock.
3. Ejercicio del banco multicliente concurrente con contador, Lock y Delay.

Para el tercer ejercicio se puede hacer manual con el client.py o ejecutar lo siguiente para que sean automaticos los 50 cliente:

for i in {1..50}; do python3 client50.py Cliente$i & done
