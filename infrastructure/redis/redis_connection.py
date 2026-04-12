import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.set(name="surname", value="Agarwal")
print(r.get("name"))
r.close()