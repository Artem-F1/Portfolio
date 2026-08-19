import redis.asyncio as redis
import json



class RedisCache:
    def __init__(self, redis_url: str, cache_ttl_seconds: int=1800):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds
        
    async def set(self, key: str, value: list | dict):
        await self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds)
        
    async def get(self, key: str) -> dict:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None
        
    async def delete(self, key) -> None:
        del_cach = await self.redis.delete(key)