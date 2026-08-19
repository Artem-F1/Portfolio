import asyncio
import time
import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select
from app.models import Task
from app.kash import RedisCache
from app.config import settings

async def run_benchmark():
    engine = create_async_engine(settings.database_url)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    cache = RedisCache(settings.redis_url, settings.cache_ttl_seconds)
    
    iterations = 500

    
    start_time = time.perf_counter()
    async with async_session_maker() as session:
        for _ in range(iterations):
            result = await session.execute(select(Task))
            _ = result.scalars().all()
    pg_duration = time.perf_counter() - start_time

    
    async with async_session_maker() as session:
        result = await session.execute(select(Task))
        tasks = result.scalars().all()
        tasks_data = [{"id": str(t.id), "title": t.title, "is_completed": t.is_completed} for t in tasks ]
        await cache.set(settings.cache_tasks_key, tasks_data)

    
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = await cache.get(settings.cache_tasks_key)
    redis_duration = time.perf_counter() - start_time

    print(f"=== Результаты бенчмарка ({iterations} итераций) ===")
    print(f"Постгрес: {pg_duration:.4f} сек. (в среднем {(pg_duration/iterations)*1000:.2f} мс/запрос)")
    print(f"Redis :     {redis_duration:.4f} сек. (в среднем {(redis_duration/iterations)*1000:.2f} мс/запрос)")
    
    if redis_duration > 0:
        multiplier = pg_duration / redis_duration
        print(f"Редис быстрее постгреса в {multiplier:.1f} раз")

    await engine.dispose()
    await cache.redis.close()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
