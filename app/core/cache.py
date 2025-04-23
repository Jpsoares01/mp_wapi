import redis.asyncio as redis
import json
from app.core.config import settings

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

async def get_weather_from_cache(city: str) -> dict | None:
    data = await r.get(city)
    if data:
        return json.loads(data)
    return None

async def set_weather_in_cache(city: str, data: dict, expire: int = 900) -> None:
    await r.set(city, json.dumps(data), ex=expire)
    