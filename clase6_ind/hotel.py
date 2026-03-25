from fastapi import FastAPI
import asyncio

app = FastAPI()

# Estado global
habitaciones_disponibles = 8
lock = asyncio.Lock() # Protege la sección crítica [cite: 27]

@app.get("/reservar")
async def reservar():
    global habitaciones_disponibles
    
    # Sección crítica protegida por Lock [cite: 15]
    async with lock:
        # Simular proceso lento (consultar BD) [cite: 12]
        await asyncio.sleep(0.2)
        
        if habitaciones_disponibles > 0:
            habitaciones_disponibles -= 1
            return {"status": "success", "mensaje": f"Reserva exitosa. Quedan {habitaciones_disponibles}"}
        else:
            return {"status": "error", "mensaje": "No hay habitaciones disponibles"}

@app.get("/estado")
async def estado():
    return {"habitaciones_disponibles": habitaciones_disponibles}

@app.post("/reiniciar")
async def reiniciar():
    global habitaciones_disponibles
    habitaciones_disponibles = 8
    return {"mensaje": "Contador reiniciado a 8"}
