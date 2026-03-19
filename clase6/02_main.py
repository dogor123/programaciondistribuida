from fastapi import FastAPI
import asyncio

app = FastAPI()

contador = 0
lock = asyncio.Lock()

@app.get("/incrementar")
async def incrementar():
    global contador

    async with lock:
        valor_actual = contador
        await asyncio.sleep(0.1)
        contador = valor_actual + 1

    return {"contador": contador}

@app.post("/reset")
async def resetear_contador():
    global contador  # variable global compartida
    contador = 0  # reiniciamos el valor
    return {"mensaje": "Contador reiniciado", "contador": contador}

