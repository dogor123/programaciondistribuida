from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI(title="Grupo 1 - Registro de Pacientes")

conexion = mysql.connector.connect(
    host="localhost",
    user="clase",
    password="1234",
    database="citas_medicas"
)

@app.post("/pacientes")
def crear_paciente(nombre: str, email: str):

    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO pacientes(nombre,email) VALUES(%s,%s)",
        (nombre,email)
    )

    conexion.commit()

    return {"mensaje":"Paciente registrado"}


