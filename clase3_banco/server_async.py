import asyncio  # Libreria para programacion asincrona

# ─── PASO 2: Variable global para contar clientes ───────────────────────────
contador_clientes = 0

# ─── PASO 4: Lock asincrono para proteger la seccion critica ────────────────
lock = asyncio.Lock()

# Funcion que maneja cada cliente (coroutine)
async def handle_client(reader, writer):
    global contador_clientes

    # Espera datos del cliente (maximo 1024 bytes)
    data = await reader.read(1024)

    # Convierte los bytes recibidos en texto
    name = data.decode()

    # ─── PASO 1: Simular tiempo de atencion bancaria (5 segundos) ───────────
    # Se usa await asyncio.sleep() en lugar de time.sleep()
    # porque time.sleep() bloquearia el servidor completo,
    # impidiendo atender a otros clientes durante la espera.
    await asyncio.sleep(5)

    # ─── PASO 4: Seccion critica protegida con lock ──────────────────────────
    # El lock garantiza que solo un cliente a la vez pueda
    # leer y modificar contador_clientes, evitando condiciones de carrera.
    async with lock:
        # ─── PASO 2: Incrementar el contador global ──────────────────────
        contador_clientes += 1
        # Captura el numero asignado dentro del lock para que sea consistente
        numero_cliente = contador_clientes

    # Construye el mensaje personalizado con el numero de cliente
    response = f"Hola {name}, eres el cliente numero {numero_cliente}"

    print(f"[Servidor] Atendiendo a {name} → cliente #{numero_cliente}")

    # Envia la respuesta al cliente (en bytes)
    writer.write(response.encode())

    # Espera a que los datos se envien completamente
    await writer.drain()

    # Cierra la conexion con el cliente
    writer.close()

# Funcion principal del servidor
async def main():
    # Crea el servidor en la IP 127.0.0.1 y puerto 5000
    # handle_client sera ejecutado por cada nueva conexion
    server = await asyncio.start_server(
        handle_client, "127.0.0.1", 5000
    )

    print("[Servidor] Banco en linea. Esperando clientes en puerto 5000...")

    # Mantiene el servidor activo
    async with server:
        # El servidor queda escuchando indefinidamente
        await server.serve_forever()

# Ejecuta el event loop principal
asyncio.run(main())

