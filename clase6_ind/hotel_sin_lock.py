from fastapi import FastAPI
import asyncio

app = FastAPI()

habitaciones_disponibles = 8

@app.get("/reservar")
async def reservar():
    global habitaciones_disponibles
    
    # --- SIN LOCK ---
    await asyncio.sleep(0.2)
    
    if habitaciones_disponibles > 0:
        habitaciones_disponibles -= 1
        return {"status": "success", "mensaje": f"Quedan {habitaciones_disponibles}"}
    else:
        return {"status": "error", "mensaje": "No hay habitaciones"}

@app.get("/estado")
async def estado():
    return {"habitaciones_disponibles": habitaciones_disponibles}
