from fastapi import FastAPI, HTTPException
from database import get_connection
import asyncio

app = FastAPI()

# 1. Crear Cita Médica (delay de 2 segundos)
@app.post("/citas")
async def crear_cita(paciente: str, fecha: str):
    conn = await get_connection()
    async with conn.cursor() as cur:
        # Simulación de proceso asíncrono
        await asyncio.sleep(2) 
        
        sql = "INSERT INTO citas (paciente, fecha, estado) VALUES (%s, %s, %s)"
        await cur.execute(sql, (paciente, fecha, 'activa'))
        await conn.commit()
    conn.close()
    return {"message": f"Cita para {paciente} creada exitosamente"}

# 2. Listar todas las citas
@app.get("/citas")
async def listar_citas():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM citas")
        result = await cur.fetchall()
    conn.close()
    return {"citas": result}

# 3. Buscar cita por paciente
@app.get("/citas/buscar/{paciente}")
async def buscar_cita(paciente: str):
    conn = await get_connection()
    async with conn.cursor() as cur:
        sql = "SELECT * FROM citas WHERE paciente = %s"
        await cur.execute(sql, (paciente,))
        result = await cur.fetchone()
    conn.close()
    
    if not result:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"cita": result}

# 4. Cancelar cita
@app.put("/citas/cancelar/{id}")
async def cancelar_cita(id: int):
    conn = await get_connection()
    async with conn.cursor() as cur:
        sql = "UPDATE citas SET estado = 'cancelada' WHERE id = %s"
        await cur.execute(sql, (id,))
        await conn.commit()
    conn.close()
    return {"message": "Cita cancelada correctamente"}

# --- ACTIVIDAD EN CLASE (NUEVOS ENDPOINTS) ---

# 5. Listar solo citas activas
@app.get("/citas/activas")
async def listar_activas():
    conn = await get_connection()
    async with conn.cursor() as cur:
        sql = "SELECT * FROM citas WHERE estado = 'activa'"
        await cur.execute(sql)
        result = await cur.fetchall()
    conn.close()
    return {"citas_activas": result}

# 6. Contar citas totales
@app.get("/citas/count")
async def contar_citas():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute("SELECT COUNT(*) as total FROM citas")
        result = await cur.fetchone()
    conn.close()
    return {"total_citas": result[0]}

# 7. Reactivar cita cancelada
@app.put("/citas/reactivar/{id}")
async def reactivar_cita(id: int):
    conn = await get_connection()
    async with conn.cursor() as cur:
        sql = "UPDATE citas SET estado = 'activa' WHERE id = %s"
        await cur.execute(sql, (id,))
        await conn.commit()
        
        # Validar si realmente se actualizó algo
        if cur.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="ID de cita no encontrado")
            
    conn.close()
    return {"message": f"Cita con ID {id} ha sido reactivada"}
