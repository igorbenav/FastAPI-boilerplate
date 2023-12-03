from typing import Union, Dict, Any

import fastapi
from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import redis.asyncio as redis
from arq import create_pool
from arq.connections import RedisSettings
import anyio

from ..api.dependencies import get_current_superuser
from .utils import queue
from .config import settings
from .db.database import Base
from .db.database import async_engine as engine
from .config import (
    DatabaseSettings, 
    RedisCacheSettings, 
    AppSettings, 
    ClientSideCacheSettings, 
    RedisQueueSettings,
    RedisRateLimiterSettings,
    EnvironmentOption,
    EnvironmentSettings
)
from ..middleware.client_cache_middleware import ClientCacheMiddleware
from .utils import cache, rate_limit

# -------------- database --------------
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -------------- cache --------------
async def create_redis_cache_pool() -> None:
    cache.pool = redis.ConnectionPool.from_url(settings.REDIS_CACHE_URL)
    cache.client = redis.Redis.from_pool(cache.pool)  # type: ignore


async def close_redis_cache_pool() -> None:
    await cache.client.aclose()


# -------------- queue --------------
async def create_redis_queue_pool() -> None:
    queue.pool = await create_pool(
        RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT)
    )


async def close_redis_queue_pool() -> None:
    await queue.pool.aclose()


# -------------- rate limit --------------
async def create_redis_rate_limit_pool() -> None:
    rate_limit.pool = redis.ConnectionPool.from_url(settings.REDIS_RATE_LIMIT_URL)
    rate_limit.client = redis.Redis.from_pool(rate_limit.pool) # type: ignore


async def close_redis_rate_limit_pool() -> None:
    await rate_limit.client.aclose()


# -------------- application --------------
async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


# -------------- application --------------
def create_application(
        router: APIRouter, 
        settings: Union[DatabaseSettings, RedisCacheSettings, AppSettings, ClientSideCacheSettings, RedisQueueSettings, RedisRateLimiterSettings, EnvironmentSettings], 
        **kwargs: Any
) -> FastAPI:

    """
    Creates and configures a FastAPI application based on the provided settings.

    This function initializes a FastAPI application, then conditionally configures 
    it with various settings and handlers. The specific configuration is determined 
    by the type of the `settings` object provided.

    Parameters
    ----------
    router : APIRouter
        The APIRouter object that contains the routes to be included in the FastAPI application.

    settings
        An instance representing the settings for configuring the FastAPI application. It determines the configuration applied:

        - AppSettings: Configures basic app metadata like name, description, contact, and license info.
        - DatabaseSettings: Adds event handlers for initializing database tables during startup.
        - RedisCacheSettings: Sets up event handlers for creating and closing a Redis cache pool.
        - ClientSideCacheSettings: Integrates middleware for client-side caching.
        - RedisQueueSettings: Sets up event handlers for creating and closing a Redis queue pool.
        - EnvironmentSettings: Conditionally sets documentation URLs and integrates custom routes for API documentation based on environment type.

    **kwargs 
        Extra keyword arguments passed directly to the FastAPI constructor.

    Returns
    -------
    FastAPI
        A fully configured FastAPI application instance.

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
    application.add_event_handler("startup", set_threadpool_tokens)

    if isinstance(settings, DatabaseSettings):
        application.add_event_handler("startup", create_tables)
    
    if isinstance(settings, RedisCacheSettings):
        application.add_event_handler("startup", create_redis_cache_pool)
        application.add_event_handler("shutdown", close_redis_cache_pool)

    if isinstance(settings, ClientSideCacheSettings):
        application.add_middleware(ClientCacheMiddleware, max_age=settings.CLIENT_CACHE_MAX_AGE)

    if isinstance(settings, RedisQueueSettings):
        application.add_event_handler("startup", create_redis_queue_pool)
        application.add_event_handler("shutdown", close_redis_queue_pool)

    if isinstance(settings, RedisRateLimiterSettings):
        application.add_event_handler("startup", create_redis_rate_limit_pool)
        application.add_event_handler("shutdown", close_redis_rate_limit_pool)

    if isinstance(settings, EnvironmentSettings):
        if settings.ENVIRONMENT != EnvironmentOption.PRODUCTION:
            docs_router = APIRouter()
            if settings.ENVIRONMENT != EnvironmentOption.LOCAL:
                docs_router = APIRouter(dependencies=[Depends(get_current_superuser)])
            
            @docs_router.get("/docs", include_in_schema=False)
            async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


            @docs_router.get("/redoc", include_in_schema=False)
            async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
                return get_redoc_html(openapi_url="/openapi.json", title="docs")


            @docs_router.get("/openapi.json", include_in_schema=False)
            async def openapi() -> Dict[str, Any]:
                out: dict = get_openapi(title=application.title, version=application.version, routes=application.routes)
                return out
            
            application.include_router(docs_router)
            
    return application
