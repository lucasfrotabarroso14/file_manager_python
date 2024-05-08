import redis
import json

class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def set_cache(self, key, value):

        json_value = json.dumps(value)
        self.redis_client.set(key, json_value)

    def get_cache(self, key):
        cached_data = self.redis_client.get(key)
        if cached_data:

            return json.loads(cached_data)
        else:
            return None

    def delete_cache(self, key):

        self.redis_client.delete(key)
