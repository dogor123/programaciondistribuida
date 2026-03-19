from fastapi import FastAPI
import asyncio

app = FastAPI()

contador = 0

@app.get("/incrementar")
async def incrementar():
    global contador

    valor_actual = contador

    # simular una operación lenta
    await asyncio.sleep(0.1)

    contador = valor_actual + 1
    return {"contador": contador}

