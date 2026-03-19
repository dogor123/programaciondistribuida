from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import pooling
import threading

app = FastAPI(title="Sistema de Chat Distribuido")

# Pool de conexiones
db_config = {
    "host": "localhost",
    "user": "clase",
    "password": "1234",
    "database": "citas_medicas"
}
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="chat_pool", pool_size=10, **db_config)

# --- 1. CHAT CENTRALIZADO (SALA) ---

@app.post("/usuarios")
def crear_usuario(nombre: str):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        return {"mensaje": f"Usuario {nombre} registrado"}
    except:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    finally:
        cursor.close()
        conn.close()

@app.get("/usuarios")
def listar_usuarios():
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

@app.post("/mensajes")
def enviar_mensaje_sala(remitente_id: int, contenido: str):
    """Mensaje para la sala común (Chat Centralizado)"""
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensajes (remitente_id, contenido) VALUES (%s, %s)",
        (remitente_id, contenido)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Enviado a la sala"}

@app.get("/mensajes")
def obtener_historial_sala():
    """Obtiene mensajes donde destinatario es NULL (públicos)"""
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mensajes WHERE destinatario_id IS NULL ORDER BY fecha ASC")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

# --- 2. CHAT PRIVADO (COMUNICACIÓN ENTRE NODOS) ---

@app.post("/mensaje_privado")
def enviar_mensaje_privado(remitente_id: int, destinatario_id: int, contenido: str):
    """Comunicación dirigida a un nodo lógico específico"""
    conn = pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensajes (remitente_id, destinatario_id, contenido) VALUES (%s, %s, %s)",
        (remitente_id, destinatario_id, contenido)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "Mensaje privado enviado"}

@app.get("/conversacion/{usuario_id}")
def obtener_privados(usuario_id: int, otro_id: int):
    """Filtra la comunicación privada entre dos nodos lógicos"""
    conn = pool.get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT * FROM mensajes 
        WHERE (remitente_id = %s AND destinatario_id = %s)
        OR (remitente_id = %s AND destinatario_id = %s)
        ORDER BY fecha ASC
    """
    cursor.execute(query, (usuario_id, otro_id, otro_id, usuario_id))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res
