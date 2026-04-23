import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.set("mensaje", "hola mundo")

print(r.get("mensaje"))
