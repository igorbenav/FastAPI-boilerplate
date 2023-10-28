from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import redis.asyncio as redis
from arq import create_pool
from arq.connections import RedisSettings

from app.api import router
from app.api.dependencies import get_current_superuser
from app.core import cache, queue
from app.core.database import Base
from app.core.database import async_engine as engine
from app.core.config import (
    settings, 
    DatabaseSettings, 
    RedisCacheSettings, 
    AppSettings, 
    ClientSideCacheSettings, 
    RedisQueueSettings,
    EnvironmentOption,
    EnvironmentSettings
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
def create_application(settings, **kwargs) -> FastAPI:
    """
    Creates and configures a FastAPI application based on the provided keyword arguments.

    The function initializes a FastAPI application and conditionally configures it
    with various settings and handlers. The configuration is determined by the type 
    of settings object provided.

    Parameters
    ----------
    settings
        The settings object can be an instance of one or more of the following:
        - AppSettings: Configures basic app information like name, description, contact, and license info.
        - DatabaseSettings: Adds event handlers related to database tables during startup.
        - RedisCacheSettings: Adds event handlers for creating and closing Redis cache pool.
        - ClientSideCacheSettings: Adds middleware for client-side caching.
        - RedisQueueSettings: Adds event handlers for creating and closing Redis queue pool.
        - EnvironmentSettings: Sets documentation URLs and sets up custom routes for documentation.
    
    **kwargs
        Additional keyword arguments that are passed directly to the FastAPI constructor.
        
    Returns
    -------
        FastAPI: A configured FastAPI application instance.
    """

    # --- before creating application ---
    if isinstance(settings, AppSettings):
        to_update = {
            "title": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "contact": {
                "name": settings.CONTACT_NAME,
                "email": settings.CONTACT_EMAIL
            },
            "license_info": {
                "name": settings.LICENSE_NAME
            }
        }
        kwargs.update(to_update)

    if isinstance(settings, EnvironmentSettings):
        kwargs.update(
            {
                "docs_url": None, 
                "redoc_url": None, 
                "openapi_url": None
            }
        )

    application = FastAPI(**kwargs)

    # --- application created ---
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

    if isinstance(settings, EnvironmentSettings):
        if settings.ENVIRONMENT is not EnvironmentOption.PRODUCTION:
            docs_router = APIRouter()
            if settings.ENVIRONMENT is not EnvironmentOption.LOCAL:
                docs_router = APIRouter(dependencies=[Depends(get_current_superuser)])
            
            @docs_router.get("/docs", include_in_schema=False)
            async def get_swagger_documentation():
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


            @docs_router.get("/redoc", include_in_schema=False)
            async def get_redoc_documentation():
                return get_redoc_html(openapi_url="/openapi.json", title="docs")


            @docs_router.get("/openapi.json", include_in_schema=False)
            async def openapi():
                return get_openapi(title=app.title, version=app.version, routes=app.routes)
            
            
            application.include_router(docs_router)
            
    return application


app = create_application(settings=settings)
