from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.post("/crear_cita")
def crear_cita():

    lock = r.set("cita_10am", "ocupado", nx=True)

    if not lock:
        raise HTTPException(status_code=400, detail="Cita ya reservada")

    return {"mensaje": "Cita creada"}
