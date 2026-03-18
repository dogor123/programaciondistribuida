from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import pooling # Para manejar múltiples conexiones
import httpx # Librería asíncrona para peticiones HTTP
import asyncio

app = FastAPI(title="Grupo 3 - Crear citas")

# Configuración de Pool de conexiones (más robusto)
dbconfig = {
    "host": "localhost",
    "user": "clase",
    "password": "1234",
    "database": "citas_medicas"
}
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

@app.post("/citas")
async def crear_cita(paciente_id: int, fecha: str):
    # 1. Petición ASÍNCRONA al otro microservicio
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"http://localhost:8002/pacientes/{paciente_id}")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Servicio de pacientes no disponible")

    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Paciente no existe")

    # El sleep de 2 segundos ahora SÍ es asíncrono y no bloquea a otros usuarios
    await asyncio.sleep(2)

    # 2. Manejo seguro de la base de datos
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        
        sql = "INSERT INTO citas (paciente_id, fecha, estado) VALUES (%s, %s, 'activa')"
        cursor.execute(sql, (paciente_id, fecha))
        
        conn.commit()
        cursor.close()
        conn.close() # Se devuelve al pool
        
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error de DB: {err}")

    return {"mensaje": "Cita creada"}
