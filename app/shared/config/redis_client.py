import redis
import json

class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set_cache(self, key, value):
        # Convertendo o valor para JSON antes de armazenar no cache
        json_value = json.dumps(value)
        self.redis_client.set(key, json_value)

    def get_cache(self, key):
        cached_data = self.redis_client.get(key)
        if cached_data:
            # Convertendo de JSON para o objeto Python antes de retornar
            return json.loads(cached_data)
        else:
            return None
