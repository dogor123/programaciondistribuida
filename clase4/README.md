# Sistema de Citas Médicas - FastAPI & MariaDB
**Asignatura:** Programación Distribuida - Clase 4
**Grupo:** Grupo 3

Este proyecto consiste en un microservicio desarrollado con FastAPI que permite la gestión de citas médicas, utilizando MariaDB como sistema de persistencia de datos de forma asíncrona.

## 🚀 Requisitos del Entorno

Para ejecutar este proyecto en WSL (Ubuntu), asegúrate de tener instalado:
* **Python 3.12+**
* **MariaDB Server**
* **Virtualenv** (opcional pero recomendado)

## 🛠️ Instalación y Configuración

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   cd clase4
Activar el entorno virtual e instalar dependencias:

Bash
source venv/bin/activate
pip install -r requirements.txt
Configurar la Base de Datos:
Accede a MariaDB y crea la estructura necesaria:

SQL
CREATE DATABASE citas_db;
USE citas_db;
CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente VARCHAR(100),
    fecha VARCHAR(50),
    estado VARCHAR(50)
);
    ```bash
  
Nota: Asegúrate de que el usuario root tenga permisos de acceso mediante mysql_native_password.

💻 Ejecución del Servidor
Para iniciar la API, ejecuta el siguiente comando desde la raíz del proyecto:

Bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
Una vez iniciado, puedes acceder a la documentación interactiva en:
👉 http://localhost:8000/docs

📌 Endpoints Implementados
Funcionalidades Base:
POST /citas: Crea una nueva cita (incluye delay de 2s para simular procesamiento distribuido).

GET /citas: Lista todas las citas registradas.

GET /citas/buscar/{paciente}: Busca citas por el nombre del paciente.

PUT /citas/cancelar/{id}: Cambia el estado de una cita a 'cancelada'.

Actividad en Clase (Nuevos):
GET /citas/activas: Filtra y muestra solo las citas con estado 'activa'.

GET /citas/count: Devuelve el número total de citas en la base de datos.

PUT /citas/reactivar/{id}: Cambia el estado de una cita cancelada de nuevo a 'activa'.

🏗️ Estructura del Proyectcto
main.py: Definición de rutas y lógica de la API.

database.py: Configuración de la conexión asíncrona con aiomysql.

requirements.txt: Dependencias del proyecto.
