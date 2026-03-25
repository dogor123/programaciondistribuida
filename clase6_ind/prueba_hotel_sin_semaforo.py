import asyncio
import httpx

# Configuración
URL_RESERVAR = "http://127.0.0.1:8000/reservar"
URL_ESTADO = "http://127.0.0.1:8000/estado"
URL_REINICIAR = "http://127.0.0.1:8000/reiniciar"

async def realizar_reserva_agresiva(client, id_cliente):
    """Lanza la petición sin esperar a nadie (sin semáforo)"""
    try:
        response = await client.get(URL_RESERVAR, timeout=10)
        data = response.json()
       
        print(f"Cliente {id_cliente}: {data.get('mensaje', 'Error')}")
    except Exception as e:
        print(f"Cliente {id_cliente}: Error de conexión ({e})")

async def main():
    async with httpx.AsyncClient() as client:
       
        await client.post(URL_REINICIAR)
        print("--- Sistema Reiniciado (8 habitaciones) ---")
        
        print("Lanzando 30 peticiones concurrentes de golpe...")
        tareas = [realizar_reserva_agresiva(client, i) for i in range(30)]
        
        await asyncio.gather(*tareas)
        
        res_final = await client.get(URL_ESTADO)
        estado = res_final.json()
        print("\n" + "="*30)
        print(f"ESTADO FINAL: {estado['habitaciones_disponibles']}")
        print("="*30)
        
        if estado['habitaciones_disponibles'] < 0:
            print("¡ÉXITO EN LA PRUEBA! Se demostró sobreventa (Race Condition).")

if __name__ == "__main__":
    asyncio.run(main())
