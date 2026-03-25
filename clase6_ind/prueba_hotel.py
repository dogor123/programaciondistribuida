import asyncio
import httpx

URL = "http://127.0.0.1:8000/reservar"
URL_ESTADO = "http://127.0.0.1:8000/estado"
SEMAFORO_LIMITE = 5 # Máximo 5 simultáneos [cite: 32]

async def realizar_reserva(client, id_cliente, semaforo):
    async with semaforo: # Adquirir permiso del semáforo [cite: 33]
        try:
            response = await client.get(URL)
            data = response.json()
            if data["status"] == "success":
                print(f"Cliente {id_cliente}: ¡Reservado! ")
            else:
                print(f"Cliente {id_cliente}: Sin disponibilidad X ")
        except Exception as e:
            print(f"Cliente {id_cliente}: Error de conexión ")

async def main():
    semaforo = asyncio.Semaphore(SEMAFORO_LIMITE)
    
    async with httpx.AsyncClient() as client:
        # Crear 30 tareas de clientes 
        tareas = [realizar_reserva(client, i, semaforo) for i in range(30)]
        
        print("Iniciando reservas concurrentes...")
        await asyncio.gather(*tareas) # Ejecución masiva [cite: 34]
        
        # Consultar estado final [cite: 22]
        res_estado = await client.get(URL_ESTADO)
        print(f"\nEstado final: {res_estado.json()}")

if __name__ == "__main__":
    asyncio.run(main())

