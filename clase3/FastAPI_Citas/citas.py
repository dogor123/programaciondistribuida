# ===============================
# IMPORTACIONES
# ===============================

from fastapi import FastAPI, HTTPException  # HTTPException para manejo de errores
from typing import List                     # Para tipado de listas
import asyncio                              # Para simular delay asíncrono


# ===============================
# CREACIÓN DE LA APLICACIÓN
# ===============================

app = FastAPI()


# ===============================
# BASE DE DATOS SIMULADA
# ===============================

citas = []  # Lista global para almacenar citas en memoria


# ===============================
# ENDPOINT RAÍZ
# ===============================

@app.get("/")
def home():
    return {"mensaje": "Sistema de Citas Médicas funcionando"}


# ===============================
# CREAR CITA (POST)
# ===============================

@app.post("/citas")
async def crear_cita(paciente: str = None, medico: str = None, fecha: str = None):

    # Validación: ningún campo puede estar vacío
    if not paciente or paciente.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre del paciente no puede estar vacío")

    if not medico or medico.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre del médico no puede estar vacío")

    if not fecha or fecha.strip() == "":
        raise HTTPException(status_code=400, detail="La fecha no puede estar vacía")

    # Simulación de delay asíncrono de 2 segundos (registro en sistema)
    await asyncio.sleep(2)

    cita = {
        "id": len(citas) + 1,
        "paciente": paciente.strip(),
        "medico": medico.strip(),
        "fecha": fecha.strip(),
        "estado": "activa"  # Estado inicial de la cita
    }

    citas.append(cita)

    return {"mensaje": "Cita creada exitosamente", "cita": cita}


# ===============================
# LISTAR CITAS (GET)
# ===============================

@app.get("/citas", response_model=List[dict])
def listar_citas():
    if len(citas) == 0:
        raise HTTPException(status_code=404, detail="No hay citas registradas")
    return citas


# ===============================
# BUSCAR CITA POR PACIENTE (GET)
# ===============================

@app.get("/citas/paciente/{nombre_paciente}")
def buscar_por_paciente(nombre_paciente: str):

    # Filtra todas las citas que coincidan con el nombre del paciente
    resultados = [
        cita for cita in citas
        if cita["paciente"].lower() == nombre_paciente.lower()  # lower() para ignorar mayúsculas
    ]

    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail=f"No se encontraron citas para el paciente '{nombre_paciente}'")

    return resultados


# ===============================
# CANCELAR CITA (DELETE)
# ===============================

@app.delete("/citas/{cita_id}")
def cancelar_cita(cita_id: int):

    for cita in citas:
        if cita["id"] == cita_id:

            # Si ya está cancelada, no tiene sentido cancelarla de nuevo
            if cita["estado"] == "cancelada":
                raise HTTPException(status_code=400, detail="La cita ya estaba cancelada")

            cita["estado"] = "cancelada"  # Cambia el estado en lugar de eliminarla
            return {"mensaje": "Cita cancelada exitosamente", "cita": cita}

    raise HTTPException(status_code=404, detail="Cita no encontrada")

