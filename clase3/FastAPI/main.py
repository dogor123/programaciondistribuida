# ===============================
# IMPORTACIONES
# ===============================

from fastapi import FastAPI, HTTPException  # HTTPException para manejo de errores
from typing import List                     # Para tipado de listas
import asyncio                              # Para simular delay asíncrono


# ===============================
# CREACIÓN DE LA APLICACIÓN
# ===============================

app = FastAPI()  # Objeto principal de la API


# ===============================
# BASE DE DATOS SIMULADA
# ===============================

clientes = []          # Lista global para almacenar clientes en memoria
contador_clientes = 0  # PUNTO 4: Contador global de clientes creados


# ===============================
# ENDPOINT RAÍZ
# ===============================

@app.get("/")
def home():
    return {"mensaje": "API del Banco funcionando"}


# ===============================
# PASO 4 – CREAR CLIENTE (POST)
# MODIFICADO: async + delay + validación + contador
# ===============================

@app.post("/clientes")
async def crear_cliente(nombre: str = None):  # None permite que llegue vacío y validemos nosotros
    global contador_clientes                   # PUNTO 4: acceder a la variable global

    # PUNTO 3: Validación básica - no permitir nombre vacío o ausente
    if not nombre or nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    # PUNTO 5: Simulación de delay asíncrono de 3 segundos
    await asyncio.sleep(3)

    # PUNTO 4: Incrementar contador global
    contador_clientes += 1

    cliente = {
        "id": len(clientes) + 1,
        "nombre": nombre.strip()  # .strip() elimina espacios al inicio y al final
    }

    clientes.append(cliente)

    return {
        "cliente": cliente,
        "total_clientes_creados": contador_clientes  # PUNTO 4: retornar el contador
    }


# ===============================
# PASO 5 – LISTAR CLIENTES (GET)
# ===============================

@app.get("/clientes", response_model=List[dict])
def listar_clientes():
    return clientes


# ===============================
# OBTENER CLIENTE POR ID (GET)
# ===============================

@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# ===============================
# PUNTO 2 – ACTUALIZAR CLIENTE (PUT)
# ===============================

@app.put("/clientes/{cliente_id}")
def actualizar_cliente(cliente_id: int, nombre: str = None):

    # PUNTO 3: Validación básica en PUT también
    if not nombre or nombre.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre no puede estar vacío")

    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente["nombre"] = nombre.strip()
            return {"mensaje": "Cliente actualizado", "cliente": cliente}

    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# ===============================
# PUNTO 1 – ELIMINAR CLIENTE (DELETE)
# ===============================

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    for i, cliente in enumerate(clientes):
        if cliente["id"] == cliente_id:
            eliminado = clientes.pop(i)  # pop() elimina el elemento en el índice i
            return {"mensaje": "Cliente eliminado", "cliente": eliminado}

    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# ===============================
# EXTRA – VER CONTADOR GLOBAL
# ===============================

@app.get("/contador")
def ver_contador():
    return {"total_clientes_creados_historicamente": contador_clientes}

