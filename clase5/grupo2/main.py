from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI(title="Grupo 2 - Consulta de Pacientes")

conexion = mysql.connector.connect(
    host="localhost",
    user="clase",
    password="1234",
    database="citas_medicas"
)

@app.get("/pacientes/{id}")
def obtener_paciente(id:int):

    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM pacientes WHERE id=%s",
        (id,)
    )

    paciente = cursor.fetchone()

    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    return paciente
