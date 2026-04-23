import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Guardar
r.set("mensaje", "hola mundo")

# Leer
print(r.get("mensaje"))
