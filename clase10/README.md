# Sistema Distribuido de Citas Médicas Basado en Eventos

**Sistemas Distribuidos – Clase 10**

## Tecnologías

| Tecnología | Rol |
|---|---|
| FastAPI | API REST (punto de entrada) |
| Redis | Lock distribuido (evita duplicados) |
| RabbitMQ | Transporte de eventos |
| AsyncIO | Concurrencia sin bloqueo |
| SQLite | Persistencia de citas y logs |

## Arquitectura

```
Cliente → FastAPI → Redis (lock)
                 ↓
           RabbitMQ (cola 'eventos')
                 ↓
         Worker(s) con AsyncIO
         ├── Notificar (async)
         ├── Registrar log (async)
         └── Auditar (async)
                 ↓
              SQLite (BD)
```

## Estructura del proyecto

```
citas_medicas/
├── main.py          # API FastAPI
├── worker.py        # Consumidor RabbitMQ
├── producer.py      # Publicador de eventos
├── redis_client.py  # Conexión Redis
├── database.py      # Base de datos SQLite
├── test_sistema.py  # Pruebas automatizadas
└── README.md
```

## Instalación

```bash
pip install fastapi uvicorn redis pika
```

## Ejecución paso a paso

### 1. Iniciar Redis
```bash
redis-server
```

### 2. Iniciar RabbitMQ
```bash
sudo service rabbitmq-server start
```

### 3. Lanzar worker(s) — Terminal(es) separadas

Worker 1:
```bash
python3 worker.py worker-1
```

Worker 2 (opcional, para distribuir carga):
```bash
python3 worker.py worker-2
```

### 4. Iniciar la API — Terminal separada
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8006
```

### 5. Explorar la API
Abrir en navegador: http://127.0.0.1:8006/docs

### 6. Ejecutar pruebas automatizadas
```bash
python3 test_system.py
```

## Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/crear_cita` | Crea una cita individual |
| POST | `/crear_citas_multiples` | Crea varias citas en paralelo |
| DELETE | `/cancelar_cita?horario=10am` | Cancela una cita activa |
| GET | `/citas` | Lista todas las citas |
| GET | `/citas/activas` | Lista solo citas activas |
| GET | `/logs` | Ver log de eventos procesados |

## Ejemplo de uso con curl

```bash
# Crear cita
curl -X POST http://127.0.0.1:8006/crear_cita \
  -H "Content-Type: application/json" \
  -d '{"horario": "10am", "paciente": "Juan Pérez"}'

# Crear múltiples citas
curl -X POST http://127.0.0.1:8006/crear_citas_multiples \
  -H "Content-Type: application/json" \
  -d '{"horarios": ["2pm", "3pm", "4pm"], "paciente": "Carlos Ruiz"}'

# Cancelar cita
curl -X DELETE "http://127.0.0.1:8006/cancelar_cita?horario=10am"

# Ver citas activas
curl http://127.0.0.1:8006/citas/activas
```

## Extensiones implementadas

- Cancelación de citas (endpoint DELETE + liberación del lock en Redis)
- Múltiples horarios (endpoint `/crear_citas_multiples` con `asyncio.gather`)
- Base de datos SQLite (tablas `citas` y `logs`)
- Múltiples workers (pasar ID como argumento: `python3 worker.py worker-2`)
- Confirmación manual de mensajes RabbitMQ (`auto_ack=False`)
- Pruebas automatizadas (`test_system.py`)


