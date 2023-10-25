from fastapi import FastAPI
import redis.asyncio as redis
from arq import create_pool
from arq.connections import RedisSettings

from app.api import router
from app.core import cache, queue
from app.core.database import Base
from app.core.database import async_engine as engine
from app.core.config import (
    settings, 
    DatabaseSettings, 
    RedisCacheSettings, 
    AppSettings, 
    ClientSideCacheSettings, 
    RedisQueueSettings
)

# -------------- database --------------
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -------------- cache --------------
async def create_redis_cache_pool():
    cache.pool = redis.ConnectionPool.from_url(settings.REDIS_CACHE_URL)
    cache.client = redis.Redis.from_pool(cache.pool)


async def close_redis_cache_pool():
    await cache.client.aclose()


# -------------- queue --------------
async def create_redis_queue_pool():
    queue.pool = await create_pool(
        RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT)
    )


async def close_redis_queue_pool():
    await queue.pool.aclose()


# -------------- application --------------
def create_application() -> FastAPI:
    if isinstance(settings, AppSettings):
        application = FastAPI(
            title=settings.APP_NAME,
            description=settings.APP_DESCRIPTION,
            contact={
                "name": settings.CONTACT_NAME,
                "email": settings.CONTACT_EMAIL
            },
            license_info={
                "name": settings.LICENSE_NAME
            }
        )
    else:
        application = FastAPI()

    application.include_router(router)
    
    if isinstance(settings, DatabaseSettings):
        application.add_event_handler("startup", create_tables)
    
    if isinstance(settings, RedisCacheSettings):
        application.add_event_handler("startup", create_redis_cache_pool)
        application.add_event_handler("shutdown", close_redis_cache_pool)

    if isinstance(settings, ClientSideCacheSettings):
        application.add_middleware(cache.ClientCacheMiddleware, max_age=60)

    if isinstance(settings, RedisQueueSettings):
        application.add_event_handler("startup", create_redis_queue_pool)
        application.add_event_handler("shutdown", close_redis_queue_pool)

    return application


app = create_application()
