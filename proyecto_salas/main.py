from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import pooling
import threading
import asyncio

app = FastAPI(title="Grupo 2 - Sistema de Reservas de Salas")

# Configuración del Pool de Conexiones (Clase 4)
db_config = {
    "host": "localhost",
    "user": "clase",
    "password": "1234",
    "database": "citas_medicas"
}
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pool_salas", pool_size=5, **db_config)

# Lock para proteger el recurso compartido (Clase 5)
# Esto evita que dos personas reserven la misma sala al mismo tiempo
lock_reserva = threading.Lock()

# --- ENDPOINTS ---

@app.post("/salas")
def crear_sala(nombre: str):
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO salas (nombre) VALUES (%s)", (nombre,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensaje": f"Sala {nombre} creada con éxito"}

@app.get("/reservas")
def listar_reservas():
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

@app.post("/reservas")
async def realizar_reserva(sala_id: int, usuario: str, fecha: str):
    # Aplicamos el concepto de la Clase 5: Sección Crítica
    with lock_reserva:
        conn = pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Verificar si la sala ya está reservada para esa fecha
        cursor.execute(
            "SELECT * FROM reservas WHERE sala_id = %s AND fecha = %s",
            (sala_id, fecha)
        )
        existe = cursor.fetchone()

        if existe:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="La sala ya está reservada para esta fecha")

        # Simular un pequeño delay de procesamiento (Clase 2 y 3)
        await asyncio.sleep(1)

        # 2. Si no existe, crear la reserva
        cursor.execute(
            "INSERT INTO reservas (sala_id, usuario, fecha) VALUES (%s, %s, %s)",
            (sala_id, usuario, fecha)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
    return {"mensaje": "Reserva realizada con éxito", "usuario": usuario, "sala": sala_id}
