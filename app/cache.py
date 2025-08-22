import redis
import json
import time
import logging

# Connexion Redis (localhost, port 6379 default)
r = redis.Redis(host="localhost", port=6379, db=0)
print(r.ping())  # Should return True if Redis is running
def get_from_cache(key: str):
    """Get a value from Redis if it exists"""
    start = time.time()
    value = r.get(key)
    if value:
        logging.info(f"Cache hit ✅ (retrieved in {time.time() - start:.4f} seconds)")
        return json.loads(value)
    return None

def set_to_cache(key: str, value, ttl: int = 60):
    """Store a value in Redis with a TTL"""
    r.setex(key, ttl, json.dumps(value))