import asyncio	# libreria para programacion asincrona
import time	# libreria para medir tiempo

async def main():
	# Abre conexion con el servidor
	reader, writer = await asyncio.open_connection(
		"127.0.0.1", 5000
	)

	# Solicita el nombre al usuario
	name = input("Ingresa tu nombre: ")

	# Guarda el tiempo inicial
	start_time = time.time()

	# Envia el nombre al servidor
	writer.write(name.encode())

	# Asegura que el mensaje se envie completamente
	await writer.drain()

	# Espera respuesta del servidor
	data = await reader.read(1024)

	# Guarda el tiempo final
	end_time = time.time()

	# Muestra respuesta
	print(data.decode())

	# Calcula el tiempo total de atencion
	print(f"Tiempo de atencion: {round(end_time - start_time, 2)} segundos")

	# Cierra la conexion
	writer.close()
	await writer.wait_closed()

# Ejectuta el cliente
asyncio.run(main())
